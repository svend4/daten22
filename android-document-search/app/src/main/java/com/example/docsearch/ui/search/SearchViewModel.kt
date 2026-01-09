package com.example.docsearch.ui.search

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.example.docsearch.data.database.DocumentDatabase
import com.example.docsearch.data.model.SearchResult
import com.example.docsearch.data.repository.DocumentRepository
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class SearchViewModel(application: Application) : AndroidViewModel(application) {

    private val repository: DocumentRepository

    private val _searchResults = MutableLiveData<List<SearchResult>>()
    val searchResults: LiveData<List<SearchResult>> = _searchResults

    private val _isSearching = MutableLiveData<Boolean>()
    val isSearching: LiveData<Boolean> = _isSearching

    private val _indexingProgress = MutableLiveData<Pair<Int, Int>>()
    val indexingProgress: LiveData<Pair<Int, Int>> = _indexingProgress

    private val _documentCount = MutableLiveData<Int>()
    val documentCount: LiveData<Int> = _documentCount

    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error

    private var searchJob: Job? = null

    init {
        val database = DocumentDatabase.getDatabase(application)
        repository = DocumentRepository(database.documentDao(), application)

        loadDocumentCount()
    }

    fun search(query: String) {
        if (query.isBlank()) {
            _searchResults.value = emptyList()
            return
        }

        // Отменить предыдущий поиск
        searchJob?.cancel()

        searchJob = viewModelScope.launch {
            try {
                _isSearching.value = true
                _error.value = null

                // Небольшая задержка для debounce
                delay(300)

                val results = repository.search(query, limit = 100)
                _searchResults.value = results

            } catch (e: Exception) {
                _error.value = "Ошибка поиска: ${e.message}"
            } finally {
                _isSearching.value = false
            }
        }
    }

    fun indexDocuments(directoryPath: String) {
        viewModelScope.launch {
            try {
                _error.value = null

                repository.indexDocuments(directoryPath) { current, total ->
                    _indexingProgress.postValue(Pair(current, total))
                }

                loadDocumentCount()

            } catch (e: Exception) {
                _error.value = "Ошибка индексации: ${e.message}"
            }
        }
    }

    fun clearIndex() {
        viewModelScope.launch {
            try {
                repository.clearIndex()
                loadDocumentCount()
                _searchResults.value = emptyList()
            } catch (e: Exception) {
                _error.value = "Ошибка очистки: ${e.message}"
            }
        }
    }

    private fun loadDocumentCount() {
        viewModelScope.launch {
            try {
                val count = repository.getDocumentCount()
                _documentCount.value = count
            } catch (e: Exception) {
                _error.value = "Ошибка загрузки: ${e.message}"
            }
        }
    }
}
