package com.example.docsearch.data.model

data class SearchResult(
    val title: String,
    val path: String,
    val snippet: String,
    val fileType: String,
    val size: Long,
    val modified: Long
) {
    val sizeInMB: String
        get() = "%.2f MB".format(size / 1024.0 / 1024.0)

    val modifiedDate: String
        get() {
            val date = java.util.Date(modified)
            val format = java.text.SimpleDateFormat("dd.MM.yyyy HH:mm", java.util.Locale.getDefault())
            return format.format(date)
        }

    val fileExtension: String
        get() = path.substringAfterLast('.', "")
}
