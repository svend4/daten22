package com.example.docsearch.data.repository

import android.content.Context
import com.example.docsearch.data.database.DocumentDao
import com.example.docsearch.data.model.SearchResult
import com.example.docsearch.utils.FileIndexer
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class DocumentRepository(
    private val documentDao: DocumentDao,
    private val context: Context
) {

    suspend fun search(query: String, limit: Int = 50): List<SearchResult> {
        return withContext(Dispatchers.IO) {
            val ftsQuery = query.split(" ")
                .filter { it.isNotBlank() }
                .joinToString(" OR ")

            documentDao.searchWithSnippet(ftsQuery, limit).map { entity ->
                SearchResult(
                    title = entity.title,
                    path = entity.path,
                    snippet = entity.content,
                    fileType = entity.fileType,
                    size = entity.size,
                    modified = entity.modified
                )
            }
        }
    }

    suspend fun indexDocuments(
        directory: String,
        onProgress: (Int, Int) -> Unit
    ) {
        withContext(Dispatchers.IO) {
            val fileIndexer = FileIndexer(context)
            fileIndexer.indexDirectory(directory, documentDao, onProgress)
        }
    }

    suspend fun getDocumentCount(): Int {
        return withContext(Dispatchers.IO) {
            documentDao.getCount()
        }
    }

    suspend fun clearIndex() {
        withContext(Dispatchers.IO) {
            documentDao.deleteAll()
        }
    }
}
