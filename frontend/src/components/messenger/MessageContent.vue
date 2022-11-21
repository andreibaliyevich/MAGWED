<script setup>
import config from '@/config.js'
</script>

<script>
export default {
  props: {
    messageType: {
      type: Object,
      required: true
    },
    msgType: {
      type: Number,
      required: true
    },
    msgContent: {
      type: [String, Object],
      required: true
    }
  },
  methods: {
    getName(path) {
      return path.split('/').at(-1)
    },
    getSize(value) {
      if (value === 0) return '0 Bytes'
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
      const i = Math.floor(Math.log(value) / Math.log(1024))
      return parseFloat((value / Math.pow(1024, i)).toFixed(1)) + ' ' + sizes[i]
    }
  }
}
</script>

<template>
  <div v-if="msgType == messageType.TEXT">
    {{ msgContent }}
  </div>
  <div v-else-if="msgType == messageType.IMAGES">
    <img
      v-for="img in msgContent"
      :src="`${ config.apiURL }${ img.content }`"
      :alt="`${ getSize(img.size) }`"
      width="150"
    >
  </div>
  <div v-else-if="msgType == messageType.FILES">
    <div
      v-for="file in msgContent"
      class="row align-items-center gx-3"
    >
      <div class="col-auto">
        <a
          :href="`${ config.apiURL }${ file.content }`"
          class="text-decoration-none"
          target="_blank"
        >
          <i class="fa-solid fa-circle-down fa-2xl"></i>
        </a>
      </div>
      <div class="col overflow-hidden">
        <h6 class="text-truncate mb-0">
          <a
            :href="`${ config.apiURL }${ file.content }`"
            class="text-decoration-none"
            target="_blank"
          >
            {{ getName(file.content) }}
          </a>
        </h6>
        <ul class="list-inline opacity-75 mb-0">
          <li class="list-inline-item">{{ getSize(file.size) }}</li>
        </ul>
      </div>
    </div>
  </div>
  <div v-else>
    Error
  </div>
</template>
