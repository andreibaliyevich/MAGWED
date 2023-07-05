<script setup>
import { reasonOfNotification } from '@/config.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

defineProps({
  notice: {
    type: Object,
    required: true
  }
})
const { getLocaleDateTimeString } = useLocaleDateTime()
</script>

<template>
  <div class="navbar-notice">
    <div class="d-flex gap-3">

      <a
        v-if="notice.initiator.profile_url"
        :href="`#${notice.initiator.profile_url}`"
        @click="$emit('clickLink')"
      >
        <UserAvatar
          :src="notice.initiator.avatar"
          :width="36"
          :height="36"
        />
      </a>
      <UserAvatar
        v-else
        :src="notice.initiator.avatar"
        :width="36"
        :height="36"
      />

      <div
        v-if="notice.reason == reasonOfNotification.FOLLOW"
        class="d-flex align-content-between flex-wrap h-100"
      >
        <p class="text-dark mb-0">
          {{ $t('notifications.follow', { user_name: notice.initiator.name }) }}
        </p>
        <small class="text-muted">
          {{ getLocaleDateTimeString(notice.created_at) }}
        </small>
      </div>
      <a
        v-else-if="notice.reason == reasonOfNotification.ARTICLE"
        :href="`#${notice.content_object.slug}`"
        @click="$emit('clickLink')"
        class="d-flex justify-content-between align-items-center text-decoration-none w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p class="text-dark mb-0">
            {{ $t('notifications.article', { user_name: notice.initiator.name, article_title: notice.content_object.translated_title }) }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <img :src="notice.content_object.thumbnail" width="64" height="64">
      </a>
      <a
        v-else-if="notice.reason == reasonOfNotification.ALBUM"
        :href="`#${notice.content_object.uuid}`"
        @click="$emit('clickLink')"
        class="d-flex justify-content-between align-items-center text-decoration-none w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p class="text-dark mb-0">
            {{ $t('notifications.album', { user_name: notice.initiator.name, album_title: notice.content_object.title }) }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <img :src="notice.content_object.thumbnail" width="64" height="64">
      </a>
      <a
        v-else-if="notice.reason == reasonOfNotification.PHOTO"
        :href="`#${notice.content_object.uuid}`"
        @click="$emit('clickLink')"
        class="d-flex justify-content-between align-items-center text-decoration-none w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p class="text-dark mb-0">
            {{ $t('notifications.photo', { user_name: notice.initiator.name }) }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <img :src="notice.content_object.thumbnail" width="64" height="64">
      </a>
      <a
        v-else-if="notice.reason == reasonOfNotification.LIKE_ALBUM"
        :href="`#${notice.content_object.uuid}`"
        @click="$emit('clickLink')"
        class="d-flex justify-content-between align-items-center text-decoration-none w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p class="text-dark mb-0">
            {{ $t('notifications.like_album', { user_name: notice.initiator.name, album_title: notice.content_object.title }) }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <img :src="notice.content_object.thumbnail" width="64" height="64">
      </a>
      <a
        v-else-if="notice.reason == reasonOfNotification.LIKE_PHOTO"
        :href="`#${notice.content_object.uuid}`"
        @click="$emit('clickLink')"
        class="d-flex justify-content-between align-items-center text-decoration-none w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p class="text-dark mb-0">
            {{ $t('notifications.like_photo', { user_name: notice.initiator.name }) }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <img :src="notice.content_object.thumbnail" width="64" height="64">
      </a>
      <a
        v-else-if="notice.reason == reasonOfNotification.COMMENT_ARTICLE"
        :href="`#${notice.content_object.slug}`"
        @click="$emit('clickLink')"
        class="d-flex justify-content-between align-items-center text-decoration-none w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p class="text-dark mb-0">
            {{ $t('notifications.comment_article', { user_name: notice.initiator.name, article_title: notice.content_object.translated_title }) }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <img :src="notice.content_object.thumbnail" width="64" height="64">
      </a>
      <a
        v-else-if="notice.reason == reasonOfNotification.COMMENT_ALBUM"
        :href="`#${notice.content_object.uuid}`"
        @click="$emit('clickLink')"
        class="d-flex justify-content-between align-items-center text-decoration-none w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p class="text-dark mb-0">
            {{ $t('notifications.comment_album', { user_name: notice.initiator.name, album_title: notice.content_object.title }) }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <img :src="notice.content_object.thumbnail" width="64" height="64">
      </a>
      <a
        v-else-if="notice.reason == reasonOfNotification.COMMENT_PHOTO"
        :href="`#${notice.content_object.uuid}`"
        @click="$emit('clickLink')"
        class="d-flex justify-content-between align-items-center text-decoration-none w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p class="text-dark mb-0">
            {{ $t('notifications.comment_photo', { user_name: notice.initiator.name }) }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <img :src="notice.content_object.thumbnail" width="64" height="64">
      </a>
      <a
        v-else-if="notice.reason == reasonOfNotification.COMMENT"
        :href="`#${notice.content_object.uuid}`"
        @click="$emit('clickLink')"
        class="d-flex justify-content-between align-items-center text-decoration-none w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p class="text-dark mb-0">
            {{ $t('notifications.comment', { user_name: notice.initiator.name }) }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <img :src="notice.content_object.thumbnail" width="64" height="64">
      </a>
      <div
        v-else-if="notice.reason == reasonOfNotification.REVIEW"
        class="d-flex align-content-between flex-wrap h-100"
      >
        <p class="text-dark mb-0">
          {{ $t('notifications.review', { user_name: notice.initiator.name }) }}
        </p>
        <small class="text-muted">
          {{ getLocaleDateTimeString(notice.created_at) }}
        </small>
      </div>

    </div>
  </div>
</template>
