<script setup>
import 'viewerjs/dist/viewer.css'
import Viewer from 'viewerjs'
import { ref, onMounted } from 'vue'
import { messageType } from '@/config.js'

const props = defineProps({
  msgType: {
    type: Number,
    required: true
  },
  msgContent: {
    type: [String, Object],
    required: true
  },
  textClass: {
    type: String,
    default: 'fs-6 text-dark'
  }
})

const messageImages = ref(null)

const getName = (path) => {
  return path.split('/').at(-1)
}

const getSize = (value) => {
  if (value === 0) return '0 Bytes'
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  const i = Math.floor(Math.log(value) / Math.log(1024))
  return parseFloat((value / Math.pow(1024, i)).toFixed(1)) + ' ' + sizes[i]
}

onMounted(() => {
  if (props.msgType === messageType.IMAGES) {
    const galleryViewer = new Viewer(messageImages.value, {
      url: 'data-original',
      transition: false,
      toolbar: {
        prev: true,
        play: true,
        next: true
      },
      title: function (image) {
        return image.alt + ' (' + (this.index + 1) + '/' + this.length + ')'
      }
    })
  }
})
</script>

<template>
  <div class="message-content">
    <div
      v-if="msgType === messageType.TEXT"
      :class="'text-pre-line ' + textClass"
    >
      {{ msgContent }}
    </div>
    <div v-else-if="msgType === messageType.IMAGES">
      <ul
        ref="messageImages"
        class="message-images"
      >
        <li v-for="img in msgContent">
          <img
            :src="img.content"
            :data-original="img.content"
            :alt="getSize(img.size)"
          >
        </li>
      </ul>
    </div>
    <div v-else-if="msgType === messageType.FILES">
      <div
        v-for="file in msgContent"
        class="row align-items-center gx-3"
      >
        <div class="col-auto">
          <a
            :href="file.content"
            :class="'text-decoration-none ' + textClass"
            target="_blank"
          >
            <i class="fa-solid fa-circle-down fa-2xl"></i>
          </a>
        </div>
        <div class="col overflow-hidden">
          <h6 class="text-truncate mb-0">
            <a
              :href="file.content"
              :class="'text-decoration-none ' + textClass"
              target="_blank"
            >
              {{ getName(file.content) }}
            </a>
          </h6>
          <ul class="list-inline opacity-75 mb-0">
            <li :class="'list-inline-item ' + textClass">
              {{ getSize(file.size) }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div v-else>
      Error
    </div>
  </div>
</template>

<style scoped>
.message-content {
  max-width: 30rem;
}

.text-pre-line {
  white-space: pre-line;
}

.message-images {
  list-style: none;
  margin: 0;
  padding: 0;
}
.message-images > li {
  display: inline-flex;
  margin: 1px;
}
.message-images > li > img {
  cursor: zoom-in;
  width: 150px;
}
</style>
