from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_upload_pdf():
    pdf_bytes = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Contents 4 0 R >>\nendobj\n"
        b"4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 72 120 Td (Hi) Tj ET\nendstream\nendobj\n"
        b"xref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000062 00000 n \n"
        b"0000000113 00000 n \n0000000212 00000 n \ntrailer\n"
        b"<< /Root 1 0 R /Size 5 >>\nstartxref\n312\n%%EOF"
    )

    files = {"file": ("sample.pdf", pdf_bytes, "application/pdf")}
    response = client.post("/upload", files=files)

    assert response.status_code == 200
    assert response.json()["filename"] == "sample.pdf"

if __name__ == "__main__":
    test_upload_pdf()
