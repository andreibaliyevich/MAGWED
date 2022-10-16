import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
  state: () => ({
    apiURL: 'http://localhost:8000',
    wsURL: 'ws://localhost:8000',
    deviceId: '',
    currency: 'USD'
  }),
  actions: {
    setDeviceId(value) {
      this.deviceId = value
    },
    setCurrency(value) {
      this.currency = value
    }
  }
})
