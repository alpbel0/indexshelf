package com.indexshelf.app.core.localization

import androidx.annotation.StringRes
import com.indexshelf.app.R

object BackendErrorStrings {
    @StringRes
    fun resourceFor(code: String): Int = when (code) {
        "unknown" -> R.string.error_unknown
        else -> R.string.error_unknown
    }
}
