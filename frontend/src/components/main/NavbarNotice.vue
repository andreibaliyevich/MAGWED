<script setup>
import { messageType, reasonOfNotification } from '@/config.js'
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

      <router-link
        v-if="notice.initiator.profile_url"
        :to="{
          name: 'OrganizerDetail',
          params: {
            locale: $i18n.locale,
            profile_url: notice.initiator.profile_url
          }
        }"
      >
        <UserAvatar
          :src="notice.initiator.avatar"
          :width="36"
          :height="36"
        />
      </router-link>
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
      <div
        v-else-if="notice.reason == reasonOfNotification.ARTICLE"
        class="d-flex justify-content-between align-items-center w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p class="text-dark mb-0">
            {{
              $t('notifications.article', {
                user_name: notice.initiator.name,
                article_title: notice.content_object.translated_title
              })
            }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <router-link
          :to="{
            name: 'ArticleDetail',
            params: {
              locale: $i18n.locale,
              slug: notice.content_object.slug
            }
          }"
        >
          <img
            :src="notice.content_object.thumbnail"
            :alt="notice.content_object.translated_title"
            width="64"
            height="64"
          >
        </router-link>
      </div>
      <div
        v-else-if="notice.reason == reasonOfNotification.ALBUM"
        class="d-flex justify-content-between align-items-center w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p class="text-dark mb-0">
            {{
              $t('notifications.album', {
                user_name: notice.initiator.name,
                album_title: notice.content_object.title
              })
            }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <router-link
          :to="{
            name: 'AlbumDetail',
            params: {
              locale: $i18n.locale,
              uuid: notice.content_object.uuid
            }
          }"
        >
          <img
            :src="notice.content_object.thumbnail"
            :alt="notice.content_object.title"
            width="64"
            height="64"
          >
        </router-link>
      </div>
      <div
        v-else-if="notice.reason == reasonOfNotification.PHOTO"
        class="d-flex justify-content-between align-items-center w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p
            v-if="notice.content_object.title"
            class="text-dark mb-0"
          >
            {{
              $t('notifications.photo_title', {
                user_name: notice.initiator.name,
                photo_title: notice.content_object.title
              })
            }}
          </p>
          <p
            v-else
            class="text-dark mb-0"
          >
            {{ $t('notifications.photo', { user_name: notice.initiator.name }) }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <router-link
          :to="{
            name: 'PhotoDetail',
            params: {
              locale: $i18n.locale,
              uuid: notice.content_object.uuid
            }
          }"
        >
          <img
            :src="notice.content_object.thumbnail"
            :alt="notice.content_object.title"
            width="64"
            height="64"
          >
        </router-link>
      </div>
      <div
        v-else-if="notice.reason == reasonOfNotification.LIKE_ALBUM"
        class="d-flex justify-content-between align-items-center w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p class="text-dark mb-0">
            {{
              $t('notifications.like_album', {
                user_name: notice.initiator.name,
                album_title: notice.content_object.title
              })
            }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <router-link
          :to="{
            name: 'AlbumDetail',
            params: {
              locale: $i18n.locale,
              uuid: notice.content_object.uuid
            }
          }"
        >
          <img
            :src="notice.content_object.thumbnail"
            :alt="notice.content_object.title"
            width="64"
            height="64"
          >
        </router-link>
      </div>
      <div
        v-else-if="notice.reason == reasonOfNotification.LIKE_PHOTO"
        class="d-flex justify-content-between align-items-center w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p
            v-if="notice.content_object.title"
            class="text-dark mb-0"
          >
            {{
              $t('notifications.like_photo_title', {
                user_name: notice.initiator.name,
                photo_title: notice.content_object.title
              })
            }}
          </p>
          <p
            v-else
            class="text-dark mb-0"
          >
            {{ $t('notifications.like_photo', { user_name: notice.initiator.name }) }}
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <router-link
          :to="{
            name: 'PhotoDetail',
            params: {
              locale: $i18n.locale,
              uuid: notice.content_object.uuid
            }
          }"
        >
          <img
            :src="notice.content_object.thumbnail"
            :alt="notice.content_object.title"
            width="64"
            height="64"
          >
        </router-link>
      </div>
      <div
        v-else-if="notice.reason == reasonOfNotification.COMMENT"
        class="d-flex justify-content-between align-items-center w-100"
      >
        <div class="d-flex align-content-between flex-wrap h-100">
          <p
            v-if="notice.content_object.content_type_model == 'article'"
            class="text-dark mb-0"
          >
            {{
              $t('notifications.comment_article', {
                user_name: notice.initiator.name,
                content: notice.content_object.content,
                article_title: notice.content_object.content_object.translated_title
              })
            }}
          </p>
          <p
            v-else-if="notice.content_object.content_type_model == 'album'"
            class="text-dark mb-0"
          >
            {{
              $t('notifications.comment_album', {
                user_name: notice.initiator.name,
                content: notice.content_object.content,
                album_title: notice.content_object.content_object.title
              })
            }}
          </p>
          <p
            v-else-if="notice.content_object.content_type_model == 'photo'"
            class="text-dark mb-0"
          >
            <div v-if="notice.content_object.content_object.title">
              {{
                $t('notifications.comment_photo_title', {
                  user_name: notice.initiator.name,
                  content: notice.content_object.content,
                  photo_title: notice.content_object.content_object.title
                })
              }}
            </div>
            <div v-else>
              {{
                $t('notifications.comment_photo', {
                  user_name: notice.initiator.name,
                  content: notice.content_object.content
                })
              }}
            </div>
          </p>
          <p
            v-else-if="notice.content_object.content_type_model == 'comment'"
            class="text-dark mb-0"
          >
            <div v-if="notice.content_object.content_object.model_name == 'article'">
              {{
                $t('notifications.comment_comment_article', {
                  user_name: notice.initiator.name,
                  content: notice.content_object.content,
                  article_title: notice.content_object.content_object.translated_title
                })
              }}
            </div>
            <div v-else-if="notice.content_object.content_object.model_name == 'album'">
              {{
                $t('notifications.comment_comment_album', {
                  user_name: notice.initiator.name,
                  content: notice.content_object.content,
                  album_title: notice.content_object.content_object.title
                })
              }}
            </div>
            <div v-else-if="notice.content_object.content_object.model_name == 'photo'">
              <div v-if="notice.content_object.content_object.title">
                {{
                  $t('notifications.comment_comment_photo_title', {
                    user_name: notice.initiator.name,
                    content: notice.content_object.content,
                    photo_title: notice.content_object.content_object.title
                  })
                }}
              </div>
              <div v-else>
                {{
                  $t('notifications.comment_comment_photo', {
                    user_name: notice.initiator.name,
                    content: notice.content_object.content
                  })
                }}
              </div>
            </div>
          </p>
          <small class="text-muted">
            {{ getLocaleDateTimeString(notice.created_at) }}
          </small>
        </div>
        <router-link
          v-if="notice.content_object.content_object.model_name == 'article'"
          :to="{
            name: 'ArticleDetail',
            params: {
              locale: $i18n.locale,
              slug: notice.content_object.content_object.slug
            }
          }"
        >
          <img
            :src="notice.content_object.content_object.thumbnail"
            :alt="notice.content_object.content_object.translated_title"
            width="64"
            height="64"
          >
        </router-link>
        <router-link
          v-else-if="notice.content_object.content_object.model_name == 'album'"
          :to="{
            name: 'AlbumDetail',
            params: {
              locale: $i18n.locale,
              uuid: notice.content_object.content_object.uuid
            }
          }"
        >
          <img
            :src="notice.content_object.content_object.thumbnail"
            :alt="notice.content_object.content_object.title"
            width="64"
            height="64"
          >
        </router-link>
        <router-link
          v-else-if="notice.content_object.content_object.model_name == 'photo'"
          :to="{
            name: 'PhotoDetail',
            params: {
              locale: $i18n.locale,
              uuid: notice.content_object.content_object.uuid
            }
          }"
        >
          <img
            :src="notice.content_object.content_object.thumbnail"
            :alt="notice.content_object.content_object.title"
            width="64"
            height="64"
          >
        </router-link>
      </div>
      <div
        v-else-if="notice.reason == reasonOfNotification.REVIEW"
        class="d-flex align-content-between flex-wrap h-100"
      >
        <p class="text-dark mb-0">
          {{ $t('notifications.review', { user_name: notice.initiator.name }) }}
          ({{ $t('reviews.rating_options', { n: notice.content_object.rating }) }}):
          {{ notice.content_object.comment }}
        </p>
        <small class="text-muted">
          {{ getLocaleDateTimeString(notice.created_at) }}
        </small>
      </div>
      <div
        v-else-if="notice.reason == reasonOfNotification.MESSAGE"
        class="d-flex align-content-between flex-wrap h-100"
      >
        <router-link
          :to="{
            name: 'Chat',
            params: {
              locale: $i18n.locale,
              uuid: notice.content_object.chat
            }
          }"
          class="text-decoration-none link-dark"
        >
          <p
            v-if="notice.content_object.msg_type == messageType.TEXT"
            class="mb-0"
          >
            {{ $t('notifications.message', { user_name: notice.initiator.name }) }}:
            {{ notice.content_object.content }}
          </p>
          <p
            v-else-if="notice.content_object.msg_type == messageType.IMAGES"
            class="mb-0"
          >
            {{ $t('notifications.message', { user_name: notice.initiator.name }) }}:
            {{ $t('messenger.images', { n: notice.content_object.content }) }}
          </p>
          <p
            v-else-if="notice.content_object.msg_type == messageType.FILES"
            class="mb-0"
          >
            {{ $t('notifications.message', { user_name: notice.initiator.name }) }}:
            {{ $t('messenger.files', { n: notice.content_object.content }) }}
          </p>
        </router-link>
        <small class="text-muted">
          {{ getLocaleDateTimeString(notice.created_at) }}
        </small>
      </div>

    </div>
  </div>
</template>
