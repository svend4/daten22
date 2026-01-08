package com.example.docsearch.utils

import android.content.Context
import android.util.Log
import com.example.docsearch.data.database.DocumentDao
import com.example.docsearch.data.database.DocumentEntity
import java.io.File

class FileIndexer(private val context: Context) {

    private val textExtractor = TextExtractor(context)
    private val supportedExtensions = setOf("txt", "pdf", "docx", "md", "log")

    suspend fun indexDirectory(
        directoryPath: String,
        dao: DocumentDao,
        onProgress: (Int, Int) -> Unit
    ) {
        val directory = File(directoryPath)
        if (!directory.exists() || !directory.isDirectory) {
            Log.e("FileIndexer", "Directory does not exist: $directoryPath")
            return
        }

        val files = collectFiles(directory)
        val totalFiles = files.size

        Log.d("FileIndexer", "Found $totalFiles files to index")

        files.forEachIndexed { index, file ->
            try {
                indexFile(file, dao)
                onProgress(index + 1, totalFiles)
            } catch (e: Exception) {
                Log.e("FileIndexer", "Error indexing ${file.name}", e)
            }
        }

        Log.d("FileIndexer", "Indexing complete")
    }

    private fun collectFiles(directory: File): List<File> {
        val files = mutableListOf<File>()

        directory.walk()
            .filter { it.isFile }
            .filter { it.extension.lowercase() in supportedExtensions }
            .filter { it.length() < 50 * 1024 * 1024 } // Пропустить файлы > 50 МБ
            .forEach { files.add(it) }

        return files
    }

    private suspend fun indexFile(file: File, dao: DocumentDao) {
        // Проверить, был ли файл уже проиндексирован
        val existing = dao.getByPath(file.absolutePath)
        if (existing != null && existing.modified == file.lastModified()) {
            Log.d("FileIndexer", "Skipping ${file.name} (already indexed)")
            return
        }

        // Извлечь текст
        val content = textExtractor.extractText(file) ?: run {
            Log.w("FileIndexer", "Could not extract text from ${file.name}")
            return
        }

        // Ограничить размер контента
        val truncatedContent = if (content.length > 1_000_000) {
            content.take(1_000_000)
        } else {
            content
        }

        // Создать entity
        val entity = DocumentEntity(
            title = file.name,
            content = truncatedContent,
            path = file.absolutePath,
            fileType = file.extension.lowercase(),
            size = file.length(),
            modified = file.lastModified()
        )

        // Вставить в базу
        dao.insert(entity)
        Log.d("FileIndexer", "Indexed: ${file.name}")
    }
}
