<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n({ useScope: 'global' })

const linksLoading = ref(true)
const socialLinks = ref([])

const socialLinkId = ref(null)
const socialLinkType = ref(null)
const socialLinkUrl = ref('')

const linkTypeOptions = ref([])

const errors = ref(null)

const btnClose = ref(null)

const setLinkTypeOptions = () => {
  linkTypeOptions.value = [
    { value: 1, text: t('auth.sociallinks.facebook') },
    { value: 2, text: t('auth.sociallinks.twitter') },
    { value: 3, text: t('auth.sociallinks.instagram') },
    { value: 4, text: t('auth.sociallinks.linkedin') },
    { value: 5, text: t('auth.sociallinks.spotify') },
    { value: 6, text: t('auth.sociallinks.youtube') },
    { value: 7, text: t('auth.sociallinks.soundcloud') },
    { value: 8, text: t('auth.sociallinks.pinterest') },
    { value: 9, text: t('auth.sociallinks.vk') }
  ]
}

const getSocialLinksData = async () => {
  try {
    const response = await axios.get('/social-links/')
    socialLinks.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    linksLoading.value = false
  }
}

const addSocialLink = async () => {
  try {
    const response = await axios.post('/social-links/', {
      link_type: socialLinkType.value,
      link_url: socialLinkUrl.value
    })
    socialLinks.value.push(response.data)
    btnClose.value.click()
    errors.value = null
  } catch (error) {
    errors.value = error.response.data
  }
}

const getSocialLinkData = async (olId) => {
  try {
    const response = await axios.get('/social-links/' + olId +'/')
    socialLinkId.value = response.data.id
    socialLinkType.value = response.data.link_type
    socialLinkUrl.value = response.data.link_url
  } catch (error) {
    console.error(error)
  }
}

const updateSocialLink = async () => {
  try {
    const response = await axios.put(
      '/social-links/' + socialLinkId.value +'/',
      {
        link_type: socialLinkType.value,
        link_url: socialLinkUrl.value
      }
    )
    const foundIndex = socialLinks.value.findIndex((element) => {
      return element.id == socialLinkId.value
    })
    socialLinks.value[foundIndex] = response.data
    btnClose.value.click()
    errors.value = null
  } catch (error) {
    errors.value = error.response.data
  }
}

const removeSocialLink = async (olId) => {
  try {
    const response = axios.delete('/social-links/' + olId +'/')
    socialLinks.value = socialLinks.value.filter((element) => {
      return element.id != olId
    })
  } catch (error) {
    console.error(error)
  }
}

const resetSocialLink = () => {
  setTimeout(() => {
    socialLinkId.value = null
    socialLinkType.value = null
    socialLinkUrl.value = ''
    errors.value = null
  }, 500)
}

watch(locale, () => {
    setLinkTypeOptions()
  })

onMounted(() => {
  setLinkTypeOptions()
  getSocialLinksData()
})
</script>

<template>
  <div class="external-links-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">
        {{ $t('auth.sociallinks.social_links') }}
      </h1>

      <LoadingIndicator v-if="linksLoading" />
      <ul
        v-else-if="socialLinks.length > 0"
        class="list-group list-group-flush"
      >
        <li
          v-for="socialLinkItem in socialLinks"
          :key="socialLinkItem.id"
          class="list-group-item"
        >
          <div class="row">
            <div class="col-3 col-md-2">
              <span
                v-if="socialLinkItem.link_type == 1"
                class="badge bg-facebook"
              >
                {{ $t('auth.sociallinks.facebook') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 2"
                class="badge bg-twitter"
              >
                {{ $t('auth.sociallinks.twitter') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 3"
                class="badge bg-instagram"
              >
                {{ $t('auth.sociallinks.instagram') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 4"
                class="badge bg-linkedin"
              >
                {{ $t('auth.sociallinks.linkedin') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 5"
                class="badge bg-spotify"
              >
                {{ $t('auth.sociallinks.spotify') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 6"
                class="badge bg-youtube"
              >
                {{ $t('auth.sociallinks.youtube') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 7"
                class="badge bg-soundcloud"
              >
                {{ $t('auth.sociallinks.soundcloud') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 8"
                class="badge bg-pinterest"
              >
                {{ $t('auth.sociallinks.pinterest') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 9"
                class="badge bg-vk"
              >
                {{ $t('auth.sociallinks.vk') }}
              </span>
            </div>
            <div class="col-6 col-md-8 overflow-hidden">
              <a
                :href="socialLinkItem.link_url"
                target="_blank"
              >
                {{ socialLinkItem.link_url }}
              </a>
            </div>
            <div class="col-3 col-md-2 d-flex justify-content-end">
              <button
                @click="getSocialLinkData(socialLinkItem.id)"
                type="button"
                class="btn btn-light btn-sm"
                data-bs-toggle="modal"
                data-bs-target="#organizerLinkModal"
              >
                <i class="fa-solid fa-pen fa-sm"></i>
              </button>
              <button
                @click="removeSocialLink(socialLinkItem.id)"
                type="button"
                class="btn btn-danger btn-sm ms-1"
              >
                <i class="fa-solid fa-trash fa-sm"></i>
              </button>
            </div>
          </div>
        </li>
      </ul>
      <div
        v-else
        class="lead"
      >
        {{ $t('auth.sociallinks.do_not_have_social_links') }}
      </div>

      <button
        class="btn btn-brand mt-4"
        type="button"
        data-bs-toggle="modal"
        data-bs-target="#organizerLinkModal"
      >
        {{ $t('auth.sociallinks.add_link') }}
      </button>

      <Teleport to="body">
        <div
          class="modal fade"
          id="organizerLinkModal"
          data-bs-backdrop="static"
          data-bs-keyboard="false"
          tabindex="-1"
          aria-labelledby="organizerLinkModalLabel"
          aria-hidden="true"
        >
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5
                  v-if="socialLinkId"
                  class="modal-title"
                  id="organizerLinkModalLabel"
                >
                  {{ $t('auth.sociallinks.changing_the_link') }}
                </h5>
                <h5
                  v-else
                  class="modal-title"
                  id="organizerLinkModalLabel"
                >
                  {{ $t('auth.sociallinks.adding_a_link') }}
                </h5>
                <button
                  @click="resetSocialLink()"
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                <form>
                  <div class="mb-3">
                    <BaseSelect
                      v-if="errors && errors.link_type"
                      v-model="socialLinkType"
                      :label="$t('auth.sociallinks.type_of_link')"
                      :options="linkTypeOptions"
                      :errors="errors.link_type"
                      id="id_link_type"
                      name="link_type"
                    />
                    <BaseSelect
                      v-else
                      v-model="socialLinkType"
                      :label="$t('auth.sociallinks.type_of_link')"
                      :options="linkTypeOptions"
                      id="id_link_type"
                      name="link_type"
                    />
                  </div>
                  <div class="mb-3">
                    <BaseInput
                      v-if="errors && errors.link_url"
                      v-model="socialLinkUrl"
                      :label="$t('auth.sociallinks.url_of_link')"
                      :errors="errors.link_url"
                      id="id_link_url"
                      name="link_url"
                      type="url"
                      maxlength="200"
                    />
                    <BaseInput
                      v-else
                      v-model="socialLinkUrl"
                      :label="$t('auth.sociallinks.url_of_link')"
                      id="id_link_url"
                      name="link_url"
                      type="url"
                      maxlength="200"
                    />
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <button
                  ref="btnClose"
                  @click="resetSocialLink()"
                  type="button"
                  class="btn btn-light"
                  data-bs-dismiss="modal"
                >
                  {{ $t('modal.close') }}
                </button>
                <button
                  v-if="socialLinkId"
                  @click="updateSocialLink()"
                  class="btn btn-brand"
                  type="button"
                >
                  {{ $t('modal.update') }}
                </button>
                <button
                  v-else
                  @click="addSocialLink()"
                  class="btn btn-brand"
                  type="button"
                >
                  {{ $t('modal.add') }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </Teleport>
    </div>
  </div>
</template>