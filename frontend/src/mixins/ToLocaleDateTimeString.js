export default {
  methods: {
    toLocaleDateTimeString(dateTimeString) {
      const dateTime = new Date(dateTimeString)
      const localeDateTime = dateTime.toLocaleTimeString(this.$i18n.locale, { timeStyle: 'short' })
        + " | " + dateTime.toLocaleDateString(this.$i18n.locale, { dateStyle: 'medium' })
      return localeDateTime
    }
  }
}
