import { defineStore } from 'pinia'

export const useConnectionBusStore = defineStore({
  id: 'connectionBus',
  state: () => ({
    user_id: null,
    online: null
  }),
  actions: {
    setUserStatus(data) {
      this.$patch({
        user_id: data.user_id,
        online: data.online
      })
    }
  }
})
