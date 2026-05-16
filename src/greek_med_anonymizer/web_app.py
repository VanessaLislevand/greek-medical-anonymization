from __future__ import annotations

from io import BytesIO
import json
from pathlib import Path
import tempfile
import zipfile

from greek_med_anonymizer.config import AppConfig, ModelConfig, PROJECT_ROOT, RuleConfig, resolve_model_dir
from greek_med_anonymizer.io_utils import read_input_text
from greek_med_anonymizer.pipeline import AnonymizationPipeline

try:
    import streamlit as st
except ImportError as exc:  # pragma: no cover
    raise RuntimeError(
        "Streamlit is not installed. Install the UI dependencies with: pip install -e '.[ui,ml]'"
    ) from exc


PROCESSING_MODE_OPTIONS = {
    "Report with template and free text": "auto",
    "Free-text-only report": "free_text_only",
    "Template-only report": "template_only",
}
DEFAULT_MODEL_DIR = "models/xlmr_phi_final"


def _build_config(
    processing_mode: str,
    mask_token: str,
    detect_phones: bool,
    detect_patient_ids: bool,
    model_dir: str,
    labels_to_mask: str,
    aggregation_strategy: str,
) -> AppConfig:
    cleaned_model_dir = model_dir.strip()
    cleaned_labels = [label.strip() for label in labels_to_mask.split(",") if label.strip()]
    return AppConfig(
        input_glob="*.docx",
        output_suffix=".anon.txt",
        mask_token=mask_token,
        processing_mode=processing_mode,
        rules=RuleConfig(
            phones=detect_phones,
            patient_ids=detect_patient_ids,
        ),
        model=ModelConfig(
            enabled=bool(cleaned_model_dir),
            model_dir=cleaned_model_dir or None,
            labels_to_mask=cleaned_labels or ["PHI"],
            aggregation_strategy=aggregation_strategy,
        ),
    )


def _entity_payload(entities: list) -> list[dict]:
    return [
        {
            "start": entity.start,
            "end": entity.end,
            "label": entity.label,
            "text": entity.text,
            "source": entity.source,
        }
        for entity in entities
    ]


def _build_output_name(filename: str) -> str:
    path = Path(filename)
    stem = path.stem
    if path.parent != Path("."):
        safe_parent = "__".join(path.parent.parts)
        return f"{safe_parent}__{stem}.anon.txt"
    return f"{stem}.anon.txt"


def _anonymize_uploaded_content(filename: str, payload: bytes, pipeline: AnonymizationPipeline) -> dict:
    suffix = Path(filename).suffix or ".txt"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(payload)
        temp_path = Path(temp_file.name)

    try:
        text = read_input_text(temp_path)
        result = pipeline.anonymize_text(text)
    finally:
        temp_path.unlink(missing_ok=True)

    metadata = _entity_payload(result.entities)
    output_name = _build_output_name(filename)
    return {
        "filename": filename,
        "output_name": output_name,
        "anonymized_text": result.anonymized_text,
        "entity_count": len(metadata),
        "preview": result.anonymized_text[:2000],
        "entities": metadata[:30],
        "metadata": metadata,
    }


def _process_uploaded_files(uploaded_files, pipeline: AnonymizationPipeline, emit_metadata: bool) -> tuple[bytes, list[dict]]:
    zip_buffer = BytesIO()
    summaries: list[dict] = []

    with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for uploaded_file in uploaded_files:
            summary = _anonymize_uploaded_content(
                uploaded_file.name,
                uploaded_file.getbuffer(),
                pipeline,
            )
            archive.writestr(summary["output_name"], summary["anonymized_text"])
            if emit_metadata:
                archive.writestr(
                    summary["output_name"] + ".json",
                    json.dumps(summary["metadata"], ensure_ascii=False, indent=2),
                )
            summaries.append(summary)

    zip_buffer.seek(0)
    return zip_buffer.getvalue(), summaries


def _process_uploaded_zip(uploaded_zip, pipeline: AnonymizationPipeline, emit_metadata: bool) -> tuple[bytes, list[dict]]:
    zip_buffer = BytesIO()
    summaries: list[dict] = []

    zip_bytes = bytes(uploaded_zip.getbuffer())
    with zipfile.ZipFile(BytesIO(zip_bytes)) as source_archive:
        with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as output_archive:
            for member_name in source_archive.namelist():
                if member_name.endswith("/"):
                    continue
                if Path(member_name).suffix.lower() not in {".docx", ".txt"}:
                    continue

                summary = _anonymize_uploaded_content(
                    member_name,
                    source_archive.read(member_name),
                    pipeline,
                )
                output_archive.writestr(summary["output_name"], summary["anonymized_text"])
                if emit_metadata:
                    output_archive.writestr(
                        summary["output_name"] + ".json",
                        json.dumps(summary["metadata"], ensure_ascii=False, indent=2),
                    )
                summaries.append(summary)

    zip_buffer.seek(0)
    return zip_buffer.getvalue(), summaries


def render_app() -> None:
    st.set_page_config(page_title="Greek Medical Report Anonymizer", layout="wide")
    st.title("Greek Medical Report Anonymizer")
    st.caption("Local web interface for anonymizing Greek medical reports.")

    model_dir = DEFAULT_MODEL_DIR
    emit_metadata = True
    use_model = True

    with st.sidebar:
        st.header("Main settings")
        processing_mode_label = st.selectbox(
            "Report type",
            list(PROCESSING_MODE_OPTIONS.keys()),
            index=0,
        )
        resolved_model_dir = resolve_model_dir(model_dir.strip()) if model_dir.strip() else None

        with st.expander("Advanced options"):
            mask_token = st.text_input("Mask token", value="[REDACTED]")

    st.markdown(
        """
        **How to use**

        1. Select the report type.
        2. Upload one or more `.docx` / `.txt` files, or upload a `.zip` file containing a folder of reports.
        3. Click **Run anonymization**.
        4. Download the generated `.zip` archive.
        """
    )

    if resolved_model_dir:
        st.caption(f"Using local model from: `{resolved_model_dir}`")

    uploaded_files = st.file_uploader(
        "Upload report(s)",
        type=["docx", "txt"],
        accept_multiple_files=True,
    )
    uploaded_zip = st.file_uploader(
        "Or upload a folder as .zip",
        type=["zip"],
        accept_multiple_files=False,
    )

    if use_model and not model_dir.strip():
        st.info("If free-text model detection is needed, please provide the local model directory.")

    has_input = bool(uploaded_files) or uploaded_zip is not None

    if st.button("Run anonymization", type="primary", disabled=not has_input):
        config = _build_config(
            processing_mode=PROCESSING_MODE_OPTIONS[processing_mode_label],
            mask_token=mask_token,
            detect_phones=True,
            detect_patient_ids=True,
            model_dir=model_dir if use_model else "",
            labels_to_mask="PHI",
            aggregation_strategy="simple",
        )

        try:
            with st.spinner("Running anonymization..."):
                pipeline = AnonymizationPipeline(config)
                if uploaded_zip is not None:
                    archive_bytes, summaries = _process_uploaded_zip(uploaded_zip, pipeline, emit_metadata)
                else:
                    archive_bytes, summaries = _process_uploaded_files(uploaded_files, pipeline, emit_metadata)
        except zipfile.BadZipFile:  # pragma: no cover
            st.error(
                "The uploaded file is not a valid .zip archive. Please create the archive with your operating system's "
                "Compress option and upload the resulting .zip file."
            )
        except Exception as exc:  # pragma: no cover
            st.error(f"Anonymization failed: {exc}")
        else:
            st.success(f"Anonymization completed for {len(summaries)} file(s).")
            st.download_button(
                "Download anonymized outputs (.zip)",
                data=archive_bytes,
                file_name="anonymized_outputs.zip",
                mime="application/zip",
            )

            for summary in summaries:
                with st.expander(f"{summary['filename']}  |  detected entities: {summary['entity_count']}"):
                    st.text_area("Preview", value=summary["preview"], height=240)
                    if summary["entities"]:
                        st.json(summary["entities"])


render_app()
