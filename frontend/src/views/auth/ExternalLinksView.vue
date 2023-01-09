<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const linksLoading = ref(true)
const organizerLinks = ref([])

const organizerLinkId = ref(null)
const organizerLinkType = ref('')
const organizerLinkUrl = ref('')

const linkTypeOptions = ref([
  { value: 'WE', text: 'Website' },
  { value: 'FK', text: 'Facebook' },
  { value: 'TR', text: 'Twitter' },
  { value: 'IM', text: 'Instagram' },
  { value: 'SY', text: 'Spotify' },
  { value: 'YE', text: 'YouTube' },
  { value: 'SD', text: 'SoundCloud' },
  { value: 'PT', text: 'Pinterest' },
  { value: 'VK', text: 'VK' },
  { value: 'LN', text: 'LinkedIn' }
])

const errors = ref(null)

const btnClose = ref(null)

const getOrganizerLinksData = async () => {
  try {
    const response = await axios.get('/accounts/auth/links/')
    organizerLinks.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    linksLoading.value = false
  }
}

const addOrganizerLink = async () => {
  try {
    const response = await axios.post('/accounts/auth/links/', {
      link_type: organizerLinkType.value,
      link_url: organizerLinkUrl.value
    })
    organizerLinks.value.push(response.data)
    btnClose.value.click()
    errors.value = null
  } catch (error) {
    errors.value = error.response.data
  }
}

const getOrganizerLinkData = async (olId) => {
  try {
    const response = await axios.get('/accounts/auth/links/' + olId +'/')
    organizerLinkId.value = response.data.id
    organizerLinkType.value = response.data.link_type
    organizerLinkUrl.value = response.data.link_url
  } catch (error) {
    console.error(error)
  }
}

const updateOrganizerLink = async () => {
  try {
    const response = await axios.put(
      '/accounts/auth/links/'
      + organizerLinkId.value +'/',
      {
        link_type: organizerLinkType.value,
        link_url: organizerLinkUrl.value
      }
    )
    const foundIndex = organizerLinks.value.findIndex((element) => {
      return element.id == organizerLinkId.value
    })
    organizerLinks.value[foundIndex] = response.data
    btnClose.value.click()
    errors.value = null
  } catch (error) {
    errors.value = error.response.data
  }
}

const removeOrganizerLink = async (olId) => {
  try {
    const response = axios.delete('/accounts/auth/links/' + olId +'/')
    organizerLinks.value = organizerLinks.value.filter((element) => {
      return element.id != olId
    })
  } catch (error) {
    console.error(error)
  }
}

const resetOrganizerLink = () => {
  setTimeout(() => {
    organizerLinkId.value = null
    organizerLinkType.value = ''
    organizerLinkUrl.value = ''
    errors.value = null
  }, 500)
}

onMounted(() => {
  getOrganizerLinksData()
})
</script>

<template>
  <div class="external-links-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">
        {{ $t('auth.externallinks.external_links') }}
      </h1>

      <LoadingIndicator v-if="linksLoading" />
      <ul
        v-else
        class="list-group list-group-flush"
      >
        <li
          v-for="organizerLinkItem in organizerLinks"
          :key="organizerLinkItem.id"
          class="list-group-item"
        >
          <div class="row">
            <div class="col-3 col-md-2">
              <span
                v-if="organizerLinkItem.link_type == 'WE'"
                class="badge bg-website"
              >
                Website
              </span>
              <span
                v-else-if="organizerLinkItem.link_type == 'FK'"
                class="badge bg-facebook"
              >
                Facebook
              </span>
              <span
                v-else-if="organizerLinkItem.link_type == 'TR'"
                class="badge bg-twitter"
              >
                Twitter
              </span>
              <span
                v-else-if="organizerLinkItem.link_type == 'IM'"
                class="badge bg-instagram"
              >
                Instagram
              </span>
              <span
                v-else-if="organizerLinkItem.link_type == 'SY'"
                class="badge bg-spotify"
              >
                Spotify
              </span>
              <span
                v-else-if="organizerLinkItem.link_type == 'YE'"
                class="badge bg-youtube"
              >
                YouTube
              </span>
              <span
                v-else-if="organizerLinkItem.link_type == 'SD'"
                class="badge bg-soundcloud"
              >
                SoundCloud
              </span>
              <span
                v-else-if="organizerLinkItem.link_type == 'PT'"
                class="badge bg-pinterest"
              >
                Pinterest
              </span>
              <span
                v-else-if="organizerLinkItem.link_type == 'VK'"
                class="badge bg-vk"
              >
                VK
              </span>
              <span
                v-else-if="organizerLinkItem.link_type == 'LN'"
                class="badge bg-linkedin"
              >
                LinkedIn
              </span>
            </div>
            <div class="col-6 col-md-8 overflow-hidden">
              <a
                :href="organizerLinkItem.link_url"
                target="_blank"
              >
                {{ organizerLinkItem.link_url }}
              </a>
            </div>
            <div class="col-3 col-md-2 d-flex justify-content-end">
              <button
                @click="getOrganizerLinkData(organizerLinkItem.id)"
                type="button"
                class="btn btn-light btn-sm"
                data-bs-toggle="modal"
                data-bs-target="#organizerLinkModal"
              >
                <i class="fa-solid fa-pen fa-sm"></i>
              </button>
              <button
                @click="removeOrganizerLink(organizerLinkItem.id)"
                type="button"
                class="btn btn-danger btn-sm ms-1"
              >
                <i class="fa-solid fa-trash fa-sm"></i>
              </button>
            </div>
          </div>
        </li>
      </ul>

      <button
        class="btn btn-brand mt-4"
        type="button"
        data-bs-toggle="modal"
        data-bs-target="#organizerLinkModal"
      >
        {{ $t('auth.externallinks.add_link') }}
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
                  v-if="!organizerLinkId"
                  class="modal-title"
                  id="organizerLinkModalLabel"
                >
                  {{ $t('auth.externallinks.adding_a_link') }}
                </h5>
                <h5
                  v-else
                  class="modal-title"
                  id="organizerLinkModalLabel"
                >
                  {{ $t('auth.externallinks.changing_the_link') }}
                </h5>
                <button
                  @click="resetOrganizerLink()"
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
                      v-model="organizerLinkType"
                      :label="$t('auth.externallinks.type_of_link')"
                      :options="linkTypeOptions"
                      :errors="errors.link_type"
                      id="id_link_type"
                      name="link_type"
                    />
                    <BaseSelect
                      v-else
                      v-model="organizerLinkType"
                      :label="$t('auth.externallinks.type_of_link')"
                      :options="linkTypeOptions"
                      id="id_link_type"
                      name="link_type"
                    />
                  </div>
                  <div class="mb-3">
                    <BaseInput
                      v-if="errors && errors.link_url"
                      v-model="organizerLinkUrl"
                      :label="$t('auth.externallinks.url_of_link')"
                      :errors="errors.link_url"
                      id="id_link_url"
                      name="link_url"
                      type="url"
                      maxlength="200"
                    />
                    <BaseInput
                      v-else
                      v-model="organizerLinkUrl"
                      :label="$t('auth.externallinks.url_of_link')"
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
                  @click="resetOrganizerLink()"
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  {{ $t('auth.externallinks.close') }}
                </button>
                <button
                  v-if="organizerLinkId"
                  @click="updateOrganizerLink()"
                  class="btn btn-brand"
                  type="button"
                >
                  {{ $t('auth.externallinks.update') }}
                </button>
                <button
                  v-else
                  @click="addOrganizerLink()"
                  class="btn btn-brand"
                  type="button"
                >
                  {{ $t('auth.externallinks.add') }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </Teleport>
    </div>
  </div>
</template>
