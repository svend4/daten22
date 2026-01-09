package com.example.docsearch.ui.adapter

import android.text.Html
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.example.docsearch.data.model.SearchResult
import com.example.docsearch.databinding.ItemSearchResultBinding

class SearchResultAdapter(
    private val onItemClick: (SearchResult) -> Unit
) : ListAdapter<SearchResult, SearchResultAdapter.ViewHolder>(DiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemSearchResultBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return ViewHolder(binding, onItemClick)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class ViewHolder(
        private val binding: ItemSearchResultBinding,
        private val onItemClick: (SearchResult) -> Unit
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(result: SearchResult) {
            binding.apply {
                textViewTitle.text = result.title
                textViewPath.text = result.path

                // Подсветка результатов (если есть HTML теги)
                textViewSnippet.text = if (result.snippet.contains("<b>")) {
                    Html.fromHtml(result.snippet, Html.FROM_HTML_MODE_LEGACY)
                } else {
                    result.snippet
                }

                textViewMeta.text = "${result.fileExtension.uppercase()} • ${result.sizeInMB} • ${result.modifiedDate}"

                root.setOnClickListener {
                    onItemClick(result)
                }
            }
        }
    }

    private class DiffCallback : DiffUtil.ItemCallback<SearchResult>() {
        override fun areItemsTheSame(oldItem: SearchResult, newItem: SearchResult): Boolean {
            return oldItem.path == newItem.path
        }

        override fun areContentsTheSame(oldItem: SearchResult, newItem: SearchResult): Boolean {
            return oldItem == newItem
        }
    }
}
