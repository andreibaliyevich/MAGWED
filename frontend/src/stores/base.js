import { defineStore } from 'pinia'

export const useBaseStore = defineStore({
  id: 'base',
  state: () => ({
    apiURL: 'http://localhost:8000'
  })
})
