<script setup>
import axios from 'axios'
import { ref, onMounted, onUnmounted } from 'vue'
import { WS_URL } from '@/config.js'
import { useSendComment } from '@/composables/sendComment.js'
import { useUserStore } from '@/stores/user.js'
import AuthorCommentItem from './AuthorCommentItem.vue'
import CommentItem from './CommentItem.vue'
import SubmitContent from './SubmitContent.vue'

const userStore = useUserStore()

const props = defineProps({
  contentType: {
    type: String,
    required: true
  },
  objectUUID: {
    type: String,
    required: true
  }
})

const commentListLoading = ref(true)
const commentList = ref([])
const commentCount = ref(0)
const nextURL = ref(null)

const commentSocket = ref(null)
const commentSocketConnect = ref(null)

const {
  newCommentSending,
  newCommentContent,
  newCommentErrors,
  sendComment
} = useSendComment(props.contentType, props.objectUUID)

const getCommentList = async () => {
  try {
    const response = await axios.get(
      '/comments/?content_type__model='
        + props.contentType
        + '&object_uuid='
        + props.objectUUID
    )
    commentList.value = response.data.results
    commentCount.value = response.data.count
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    commentListLoading.value = false
  }
}

const getMoreCommentList = async () => {
  commentListLoading.value = true
  try {
    const response = await axios.get(nextURL.value)
    commentList.value = [...commentList.value, ...response.data.results]
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    commentListLoading.value = false
  }
}

const getCommentListOfComment = (inList) => {
  let outList = []
  for (let i = 0; i < inList.length; i++) {
    outList.push(inList[i])

    if (inList[i].comments.length > 0) {
      outList.push(...getCommentListOfComment(inList[i].comments))
    }
  }
  return outList
}

const addCommentToList = (cList, data) => {
  for (let i = 0; i < cList.length; i++) {
    if (cList[i].uuid == data.comment_uuid) {
      cList[i].comments.push(data.instance)
      return true
    } else if (cList[i].comments.length > 0) {
      const result = addCommentToList(cList[i].comments, data)
      if (result) {
        return true
      }
    }
  }
  return false
}

const updateCommentFromList = (cList, data) => {
  for (let i = 0; i < cList.length; i++) {
    if (cList[i].uuid == data.uuid) {
      cList[i].content = data.content
      return true
    } else if (cList[i].comments.length > 0) {
      const result = updateCommentFromList(cList[i].comments, data)
      if (result) {
        return true
      }
    }
  }
  return false
}

const removeCommentFromList = (cList, data) => {
  for (let i = 0; i < cList.length; i++) {
    if (cList[i].uuid == data) {
      return [true, true]
    } else if (cList[i].comments.length > 0) {
      const result = removeCommentFromList(cList[i].comments, data)
      if (result[0]) {
        if (result[1]) {
          cList[i].comments = cList[i].comments.filter((element) => {
            return element.uuid != data
          })
          return [true, false]
        } else {
          return [true, false]
        }
      }
    }
  }
  return [false, false]
}

const openCommentSocket = async () => {
  commentSocket.value = new WebSocket(
    WS_URL
      + '/ws/comments/'
      + props.contentType
      + '/'
      + props.objectUUID
      + '/'
  )
  commentSocket.value.onopen = (event) => {
    commentSocketConnect.value = true
  }
  commentSocket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.action == 'create') {
      if (!!data.data.comment_uuid) {
        addCommentToList(commentList.value, data.data)
      } else {
        commentList.value.push(data.data.instance)
        commentCount.value += 1
      }
    } else if (data.action == 'update') {
      updateCommentFromList(commentList.value, data.data)
    } else if (data.action == 'destroy') {
      const result = removeCommentFromList(commentList.value, data.data)
      if (result[0] && result[1]) {
        commentList.value = commentList.value.filter((element) => {
          return element.uuid != data.data
        })
        commentCount.value -= 1
      }
    }
  }
  commentSocket.value.onclose = (event) => {
    commentSocket.value = null
    commentSocketConnect.value = false
  }
  commentSocket.value.onerror = (error) => {
    commentSocket.value = null
    commentSocketConnect.value = false
  }
}

const closeCommentSocket = () => {
  if (commentSocket.value) {
    commentSocket.value.close()
  }
}

onMounted(() => {
  getCommentList()
  openCommentSocket()
})

onUnmounted(() => {
  closeCommentSocket()
})
</script>

<template>
  <div class="comment-list">
    <h1 class="h5 text-center">
      {{ $t('comments.comments') }} ({{ commentCount }})
    </h1>

    <div v-if="commentList.length > 0">
      <TransitionGroup
        tag="ul"
        name="list-group"
        class="list-group list-group-flush"
      >
        <li
          v-for="commentItem in commentList"
          :key="commentItem.uuid"
          class="list-group-item"
        >
          <AuthorCommentItem
            v-if="userStore.uuid == commentItem.author.uuid"
            :commentItem="commentItem"
          />
          <CommentItem
            v-else
            :commentItem="commentItem"
          />
          <TransitionGroup
            v-if="commentItem.comments.length > 0"
            tag="ul"
            name="list-group"
            class="list-group list-group-flush"
          >
            <li
              v-for="commentOfCommentItem in getCommentListOfComment(commentItem.comments)"
              :key="commentOfCommentItem.uuid"
              class="list-group-item"
            >
              <AuthorCommentItem
                v-if="userStore.uuid == commentOfCommentItem.author.uuid"
                :commentItem="commentOfCommentItem"
              />
              <CommentItem
                v-else
                :commentItem="commentOfCommentItem"
              />
            </li>
          </TransitionGroup>
        </li>
      </TransitionGroup>
    </div>
    <div
      v-else-if="!commentListLoading"
      class="lead d-flex justify-content-center py-3"
    >
      {{ $t('organizers.no_reviews') }}
    </div>
    <div v-if="nextURL" v-intersection="getMoreCommentList"></div>
    <LoadingIndicator v-if="commentListLoading" />

    <form
      @submit.prevent="sendComment()"
      class="mt-3 mx-lg-5"
    >
      <SubmitContent
        v-model="newCommentContent"
        :loadingStatus="newCommentSending"
        id="id_new_content"
        :placeholder="$t('comments.add_comment')"
        :errors="newCommentErrors?.content ? newCommentErrors.content : []"
      />
    </form>
  </div>
</template>

<style scoped>
.list-group-enter-active,
.list-group-leave-active {
  transition: all 0.5s;
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
  -ms-transition: all 0.5s;
  -o-transition: all 0.5s;
}
.list-group-enter-from,
.list-group-leave-to {
  opacity: 0;
  transform: translateY(+30px);
}
</style>
