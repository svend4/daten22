package com.example.docsearch

import android.app.Application
import com.tom_roush.pdfbox.android.PDFBoxResourceLoader

class DocumentSearchApp : Application() {

    override fun onCreate() {
        super.onCreate()

        // Инициализация PDFBox
        PDFBoxResourceLoader.init(applicationContext)
    }
}
