export const API_URL = 'http://localhost:8000'
export const WS_URL = 'ws://localhost:8000'

export const LANGUAGES = [
  { value: 'en', text: 'English' },
  { value: 'ru', text: 'Русский' },
  { value: 'be', text: 'Беларуская' },
  { value: 'uk', text: 'Українська' }
]

export const CURRENCIES = [
  { value: 'USD', text: '$' },
  { value: 'EUR', text: '€' },
  { value: 'RUB', text: '₽' },
  { value: 'BYN', text: 'Br' },
  { value: 'UAH', text: '₴' }
]

export const userType = {
  ADMIN: 1,
  CUSTOMER: 2,
  ORGANIZER: 3
}

export const chatType = {
  DIALOG: 1,
  GROUP: 2
}

export const messageType = {
  TEXT: 1,
  IMAGES: 2,
  FILES: 3
}

export const reasonOfNotification = {
  FOLLOW: 1,
  ARTICLE: 2,
  ALBUM: 3,
  PHOTO: 4,
  LIKE_ALBUM: 5,
  LIKE_PHOTO: 6,
  COMMENT_ARTICLE: 7,
  COMMENT_ALBUM: 8,
  COMMENT_PHOTO: 9,
  COMMENT: 10,
  REVIEW: 11
}
