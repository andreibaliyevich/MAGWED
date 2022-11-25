export default function useLocaleDateTime() {
  const getLocaleDateTimeString = (locale, dateTimeString) => {
    const dateTime = new Date(dateTimeString)
    return dateTime.toLocaleTimeString(locale, {
      timeStyle: 'short'
    }) + " | " + dateTime.toLocaleDateString(locale, {
      dateStyle: 'medium'
    })
  }
  return getLocaleDateTimeString
}
