from scanner import TCPPortScanner
from report import PDFReportExporter, JSONReportExporter


def main():
    print("=== APLIKASI PORT SCANNER OOP ===")

    host = input(
        "Masukkan IP atau Domain target (contoh: 127.0.0.1): "
    ).strip()

    try:
        start_port = int(
            input("Masukkan port awal (contoh: 1): ")
        )

        end_port = int(
            input("Masukkan port akhir (contoh: 1024): ")
        )

    except ValueError:
        print("[!] Port harus berupa angka.")
        return

    # Membuat objek scanner
    scanner = TCPPortScanner(
        host,
        start_port,
        end_port
    )

    # Menjalankan scan
    scan_result = scanner.scan()

    # Nama file output
    safe_host = host.replace(".", "_")

    pdf_filename = (
        f"scan_report_{safe_host}.pdf"
    )

    json_filename = (
        f"scan_report_{safe_host}.json"
    )

    # Membuat objek exporter
    pdf_exporter = PDFReportExporter(
        scan_result,
        pdf_filename
    )

    json_exporter = JSONReportExporter(
        scan_result,
        json_filename
    )

    # Polymorphism:
    # semua exporter dipanggil dengan method export()
    exporters = [
        pdf_exporter,
        json_exporter
    ]

    for exporter in exporters:
        exporter.export()

    print("\n[+] Proses selesai.")


if __name__ == "__main__":
    main()