<script setup>
import axios from 'axios'

const props = defineProps({
  objFavorite: {
    type: Boolean,
    required: true
  },
  contentType: {
    type: String,
    required: true
  },
  objectUUID: {
    type: String,
    required: true
  }
})
const emit = defineEmits(['updateFavorite'])

const addToFavorites = async () => {
  try {
    const response = await axios.post('/social/favorite/', {
      content_type: props.contentType,
      object_uuid: props.objectUUID
    })
    if (response.status === 201) {
      emit('updateFavorite', true)
    }
  } catch (error) {
    console.error(error)
  }
}

const removeFromFavorites = async () => {
  try {
    const response = await axios.delete('/social/favorite/', {
      data: {
        content_type: props.contentType,
        object_uuid: props.objectUUID
      }
    })
    if (response.status === 204) {
      emit('updateFavorite', false)
    }
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <div class="favorite-dropdown-item">
    <button
      v-if="objFavorite"
      @click="removeFromFavorites()"
      type="button"
      class="dropdown-item btn btn-link"
    >
      <i class="fa-solid fa-star"></i>
      {{ $t('favorites.remove_from_favourites') }}
    </button>
    <button
      v-else
      @click="addToFavorites()"
      type="button"
      class="dropdown-item btn btn-link"
    >
      <i class="fa-regular fa-star"></i>
      {{ $t('favorites.add_to_favourites') }}
    </button>
  </div>
</template>
