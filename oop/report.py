from abc import ABC, abstractmethod
import json
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


class BaseReportExporter(ABC):
    """Abstract class exporter laporan."""

    def __init__(self, scan_result, filename):
        self._scan_result = scan_result
        self._filename = filename

    @abstractmethod
    def export(self):
        pass


class PDFReportExporter(BaseReportExporter):
    """Exporter laporan PDF."""

    def export(self):
        doc = SimpleDocTemplate(
            self._filename,
            pagesize=letter
        )

        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "TitleStyle",
            parent=styles["Heading1"],
            fontSize=18,
            textColor=colors.HexColor("#1a365d"),
            alignment=1,
        )

        story.append(
            Paragraph(
                "Laporan Hasil Pemindaian Port",
                title_style,
            )
        )
        story.append(Spacer(1, 12))

        summary_data = [
            ["Target Host", self._scan_result["host"]],
            ["Target IP", self._scan_result["ip"]],
            [
                "Rentang Port",
                f"{self._scan_result['start_port']} - {self._scan_result['end_port']}",
            ],
            ["Waktu", str(datetime.now())],
        ]

        summary_table = Table(summary_data, colWidths=[120, 350])

        summary_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
                ]
            )
        )

        story.append(summary_table)
        story.append(Spacer(1, 15))

        open_ports = self._scan_result["open_ports"]

        if open_ports:
            data = [["Port", "Status"]]

            for port in open_ports:
                data.append([str(port), "TERBUKA"])

            port_table = Table(data)

            port_table.setStyle(
                TableStyle(
                    [
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                    ]
                )
            )

            story.append(port_table)

        else:
            story.append(
                Paragraph(
                    "Tidak ditemukan port terbuka.",
                    styles["Normal"],
                )
            )

        doc.build(story)

        print(
            f"[+] Laporan PDF berhasil dibuat: {self._filename}"
        )


class JSONReportExporter(BaseReportExporter):
    """Exporter laporan JSON."""

    def export(self):
        data = {
            "target_host": self._scan_result["host"],
            "target_ip": self._scan_result["ip"],
            "port_range": {
                "start": self._scan_result["start_port"],
                "end": self._scan_result["end_port"],
            },
            "scan_time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "total_open_ports": len(
                self._scan_result["open_ports"]
            ),
            "open_ports": self._scan_result["open_ports"],
        }

        with open(
            self._filename,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                data,
                f,
                indent=4,
            )

        print(
            f"[+] Laporan JSON berhasil dibuat: {self._filename}"
        )