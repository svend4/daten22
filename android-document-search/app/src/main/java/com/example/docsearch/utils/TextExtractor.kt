package com.example.docsearch.utils

import android.content.Context
import android.util.Log
import com.tom_roush.pdfbox.android.PDFBoxResourceLoader
import com.tom_roush.pdfbox.pdmodel.PDDocument
import com.tom_roush.pdfbox.text.PDFTextStripper
import org.apache.poi.xwpf.usermodel.XWPFDocument
import java.io.File
import java.io.FileInputStream

class TextExtractor(private val context: Context) {

    init {
        // Инициализация PDFBox для Android
        PDFBoxResourceLoader.init(context)
    }

    fun extractText(file: File): String? {
        return try {
            when (file.extension.lowercase()) {
                "txt", "md", "log" -> extractTextFromPlainText(file)
                "pdf" -> extractTextFromPdf(file)
                "docx" -> extractTextFromDocx(file)
                else -> null
            }
        } catch (e: Exception) {
            Log.e("TextExtractor", "Error extracting text from ${file.name}", e)
            null
        }
    }

    private fun extractTextFromPlainText(file: File): String {
        return file.readText(Charsets.UTF_8)
    }

    private fun extractTextFromPdf(file: File): String {
        val document = PDDocument.load(file)
        val stripper = PDFTextStripper()

        // Ограничить количество страниц для больших PDF
        if (document.numberOfPages > 100) {
            stripper.endPage = 100
        }

        val text = stripper.getText(document)
        document.close()

        return text
    }

    private fun extractTextFromDocx(file: File): String {
        FileInputStream(file).use { fis ->
            val document = XWPFDocument(fis)
            val text = StringBuilder()

            // Извлечь текст из параграфов
            document.paragraphs.forEach { paragraph ->
                text.append(paragraph.text)
                text.append("\n")
            }

            // Извлечь текст из таблиц
            document.tables.forEach { table ->
                table.rows.forEach { row ->
                    row.tableCells.forEach { cell ->
                        text.append(cell.text)
                        text.append(" ")
                    }
                    text.append("\n")
                }
            }

            document.close()
            return text.toString()
        }
    }
}
