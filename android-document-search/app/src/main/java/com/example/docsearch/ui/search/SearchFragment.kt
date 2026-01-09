package com.example.docsearch.ui.search

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.appcompat.widget.SearchView
import androidx.core.content.FileProvider
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.docsearch.databinding.FragmentSearchBinding
import com.example.docsearch.ui.adapter.SearchResultAdapter
import java.io.File

class SearchFragment : Fragment() {

    private var _binding: FragmentSearchBinding? = null
    private val binding get() = _binding!!

    private val viewModel: SearchViewModel by viewModels()
    private lateinit var adapter: SearchResultAdapter

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentSearchBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        setupRecyclerView()
        setupSearchView()
        setupButtons()
        observeViewModel()
    }

    private fun setupRecyclerView() {
        adapter = SearchResultAdapter { result ->
            openDocument(result.path)
        }

        binding.recyclerView.apply {
            layoutManager = LinearLayoutManager(context)
            adapter = this@SearchFragment.adapter
        }
    }

    private fun setupSearchView() {
        binding.searchView.setOnQueryTextListener(object : SearchView.OnQueryTextListener {
            override fun onQueryTextSubmit(query: String?): Boolean {
                return false
            }

            override fun onQueryTextChange(newText: String?): Boolean {
                newText?.let { viewModel.search(it) }
                return true
            }
        })
    }

    private fun setupButtons() {
        binding.buttonIndex.setOnClickListener {
            val documentsPath = Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_DOCUMENTS
            ).absolutePath

            viewModel.indexDocuments(documentsPath)

            Toast.makeText(context, "Индексация начата...", Toast.LENGTH_SHORT).show()
        }

        binding.buttonClear.setOnClickListener {
            viewModel.clearIndex()
            Toast.makeText(context, "Индекс очищен", Toast.LENGTH_SHORT).show()
        }
    }

    private fun observeViewModel() {
        viewModel.searchResults.observe(viewLifecycleOwner) { results ->
            adapter.submitList(results)

            binding.textViewResults.text = if (results.isEmpty()) {
                "Ничего не найдено"
            } else {
                "Найдено: ${results.size}"
            }
        }

        viewModel.isSearching.observe(viewLifecycleOwner) { isSearching ->
            binding.progressBar.visibility = if (isSearching) View.VISIBLE else View.GONE
        }

        viewModel.indexingProgress.observe(viewLifecycleOwner) { (current, total) ->
            binding.textViewProgress.text = "Индексация: $current / $total"
            binding.textViewProgress.visibility = View.VISIBLE

            if (current == total) {
                binding.textViewProgress.postDelayed({
                    binding.textViewProgress.visibility = View.GONE
                }, 2000)
            }
        }

        viewModel.documentCount.observe(viewLifecycleOwner) { count ->
            binding.textViewDocCount.text = "Документов в индексе: $count"
        }

        viewModel.error.observe(viewLifecycleOwner) { error ->
            error?.let {
                Toast.makeText(context, it, Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun openDocument(path: String) {
        try {
            val file = File(path)
            val uri = FileProvider.getUriForFile(
                requireContext(),
                "${requireContext().packageName}.fileprovider",
                file
            )

            val intent = Intent(Intent.ACTION_VIEW).apply {
                setDataAndType(uri, getMimeType(file.extension))
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }

            startActivity(intent)

        } catch (e: Exception) {
            Toast.makeText(
                context,
                "Не удалось открыть файл: ${e.message}",
                Toast.LENGTH_SHORT
            ).show()
        }
    }

    private fun getMimeType(extension: String): String {
        return when (extension.lowercase()) {
            "pdf" -> "application/pdf"
            "txt", "md", "log" -> "text/plain"
            "docx" -> "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            else -> "*/*"
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
