package com.indexshelf.app

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.activity.compose.setContent
import androidx.lifecycle.lifecycleScope
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.ui.res.stringResource
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.foundation.layout.fillMaxSize
import dagger.hilt.android.AndroidEntryPoint
import com.indexshelf.app.core.datastore.LocalePreferences
import com.indexshelf.app.core.localization.AppLocaleManager
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

@AndroidEntryPoint
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val localeManager = AppLocaleManager(this)
        lifecycleScope.launch {
            LocalePreferences(applicationContext).localeTag(null).first()?.let(localeManager::apply)
        }
        setContent { IndexShelfStartup() }
    }
}

@Composable
@Suppress("FunctionNaming")
fun IndexShelfStartup(modifier: Modifier = Modifier) {
    Surface(modifier = modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
        Text(text = stringResource(StartupState.WelcomeMessage))
    }
}
