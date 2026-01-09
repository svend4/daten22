package com.example.docsearch.data.database

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.Fts4

@Fts4
@Entity(tableName = "documents_fts")
data class DocumentEntity(
    @ColumnInfo(name = "title")
    val title: String,

    @ColumnInfo(name = "content")
    val content: String,

    @ColumnInfo(name = "path")
    val path: String,

    @ColumnInfo(name = "file_type")
    val fileType: String,

    @ColumnInfo(name = "size")
    val size: Long,

    @ColumnInfo(name = "modified")
    val modified: Long
)
