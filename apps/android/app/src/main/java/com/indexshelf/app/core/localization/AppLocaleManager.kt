package com.indexshelf.app.core.localization

import android.app.LocaleManager
import android.content.Context
import android.os.Build
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.os.LocaleListCompat

class AppLocaleManager(private val context: Context) {
    fun apply(localeTag: String?) {
        require(localeTag == null || localeTag in SUPPORTED_LOCALE_TAGS) {
            "Unsupported locale: $localeTag"
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            context.getSystemService(LocaleManager::class.java).applicationLocales =
                android.os.LocaleList.forLanguageTags(localeTag.orEmpty())
        } else {
            AppCompatDelegate.setApplicationLocales(LocaleListCompat.forLanguageTags(localeTag.orEmpty()))
        }
    }

    private companion object {
        val SUPPORTED_LOCALE_TAGS = setOf("en", "tr")
    }
}
