package com.example.docsearch.data.database

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface DocumentDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(document: DocumentEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(documents: List<DocumentEntity>)

    @Query("DELETE FROM documents_fts")
    suspend fun deleteAll()

    @Query("DELETE FROM documents_fts WHERE path = :path")
    suspend fun deleteByPath(path: String)

    @Query("SELECT COUNT(*) FROM documents_fts")
    suspend fun getCount(): Int

    @Query("""
        SELECT * FROM documents_fts
        WHERE documents_fts MATCH :query
        ORDER BY rank
        LIMIT :limit
    """)
    fun search(query: String, limit: Int = 50): Flow<List<DocumentEntity>>

    @Query("""
        SELECT
            title,
            path,
            file_type,
            size,
            modified,
            snippet(documents_fts, 1, '<b>', '</b>', '...', 30) as content
        FROM documents_fts
        WHERE documents_fts MATCH :query
        ORDER BY rank
        LIMIT :limit
    """)
    suspend fun searchWithSnippet(query: String, limit: Int = 50): List<DocumentEntity>

    @Query("SELECT * FROM documents_fts WHERE path = :path LIMIT 1")
    suspend fun getByPath(path: String): DocumentEntity?

    @Query("SELECT DISTINCT file_type FROM documents_fts")
    suspend fun getAllFileTypes(): List<String>
}
