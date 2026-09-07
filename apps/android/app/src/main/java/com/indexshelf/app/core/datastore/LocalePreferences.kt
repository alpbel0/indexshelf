package com.indexshelf.app.core.datastore

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.localeDataStore: DataStore<Preferences> by preferencesDataStore(name = "locale_preferences")

class LocalePreferences(private val context: Context) {
    fun localeTag(principalId: String?): Flow<String?> = context.localeDataStore.data.map { preferences ->
        preferences[preferenceKey(principalId)]
    }

    suspend fun setLocaleTag(principalId: String?, localeTag: String) {
        require(localeTag in SUPPORTED_LOCALE_TAGS) { "Unsupported locale: $localeTag" }
        context.localeDataStore.edit { preferences ->
            preferences[preferenceKey(principalId)] = localeTag
        }
    }

    private fun preferenceKey(principalId: String?) =
        stringPreferencesKey(principalId?.let { "locale.principal.$it" } ?: "locale.device")

    private companion object {
        val SUPPORTED_LOCALE_TAGS = setOf("en", "tr")
    }
}
