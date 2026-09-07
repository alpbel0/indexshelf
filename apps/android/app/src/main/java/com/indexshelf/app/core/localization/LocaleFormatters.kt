package com.indexshelf.app.core.localization

import android.content.Context
import java.math.BigDecimal
import java.text.NumberFormat
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.util.Currency
import java.util.Locale

object LocaleFormatters {
    fun savedItems(context: Context, count: Int): String =
        context.resources.getQuantityString(com.indexshelf.app.R.plurals.saved_items, count, count)

    fun date(instant: Instant, locale: Locale): String =
        DateTimeFormatter.ofPattern("dd MMM yyyy", locale).withZone(ZoneId.systemDefault()).format(instant)

    fun number(value: BigDecimal, locale: Locale): String =
        NumberFormat.getNumberInstance(locale).format(value)

    fun currency(value: BigDecimal, currencyCode: String, locale: Locale): String =
        NumberFormat.getCurrencyInstance(locale).apply {
            currency = Currency.getInstance(currencyCode)
        }.format(value)
}
