<script setup>
const getYears = () => {
  let result = []
  let currentYear = new Date().getFullYear()
  for (let i = 2021; i <= currentYear; i++) {
    result.push(i)
  }
  return result
}
</script>

<template>
  <div class="base-blog-view">
    <div class="container my-5">
      <button
        type="button"
        class="btn btn-light border w-100 mb-5 d-lg-none"
        data-bs-toggle="offcanvas"
        data-bs-target="#filter_menu"
        aria-controls="filter_menu"
      >
        {{ $t('blog.filters') }}
        <i class="fa-solid fa-filter"></i>
      </button>
      <div class="row">
        <div class="col-lg-8">
          <router-view></router-view>
        </div>
        <div class="col-lg-4">
          <div
            id="filter_menu"
            tabindex="-1"
            class="offcanvas-lg offcanvas-end"
            aria-labelledby="filter_menu_label"
          >
            <div class="offcanvas-header border-bottom">
              <h5
                id="filter_menu_label"
                class="offcanvas-title"
              >
                {{ $t('blog.filters') }}
              </h5>
              <button
                ref="filterMenuClose"
                type="button"
                class="btn-close"
                data-bs-dismiss="offcanvas"
                data-bs-target="#filter_menu"
                aria-label="Close"
              ></button>
            </div>
            <div class="offcanvas-body border border-light rounded shadow-sm d-lg-block py-lg-4 px-4">
              <h6 class="lead fw-bold">{{ $t('blog.categories') }}</h6>
              <ul class="nav nav-pills justify-content-center mb-3">
                <li
                  :class="[
                    'nav-item',
                    $route.query.category === 'design' ? 'active' : null
                  ]"
                >
                  <router-link
                    :to="{
                      name: 'ArticleList',
                      query: {
                        author: $route.query.author,
                        category: 'design',
                        year: $route.query.year
                      }
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      $route.query.category === 'design' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.design') }}
                  </router-link>
                </li>
                <li
                  :class="[
                    'nav-item',
                    $route.query.category === 'fashion' ? 'active' : null
                  ]"
                >
                  <router-link
                    :to="{
                      name: 'ArticleList',
                      query: {
                        author: $route.query.author,
                        category: 'fashion',
                        year: $route.query.year
                      }
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      $route.query.category === 'fashion' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.fashion') }}
                  </router-link>
                </li>
                <li
                  :class="[
                    'nav-item',
                    $route.query.category === 'inspiration' ? 'active' : null
                  ]"
                >
                  <router-link
                    :to="{
                      name: 'ArticleList',
                      query: {
                        author: $route.query.author,
                        category: 'inspiration',
                        year: $route.query.year
                      }
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      $route.query.category === 'inspiration' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.inspiration') }}
                  </router-link>
                </li>
                <li
                  :class="[
                    'nav-item',
                    $route.query.category === 'journey' ? 'active' : null
                  ]"
                >
                  <router-link
                    :to="{
                      name: 'ArticleList',
                      query: {
                        author: $route.query.author,
                        category: 'journey',
                        year: $route.query.year
                      }
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      $route.query.category === 'journey' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.journey') }}
                  </router-link>
                </li>
                <li
                  :class="[
                    'nav-item',
                    $route.query.category === 'lifestyle' ? 'active' : null
                  ]"
                >
                  <router-link
                    :to="{
                      name: 'ArticleList',
                      query: {
                        author: $route.query.author,
                        category: 'lifestyle',
                        year: $route.query.year
                      }
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      $route.query.category === 'lifestyle' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.lifestyle') }}
                  </router-link>
                </li>
                <li
                  :class="[
                    'nav-item',
                    $route.query.category === 'photography' ? 'active' : null
                  ]"
                >
                  <router-link
                    :to="{
                      name: 'ArticleList',
                      query: {
                        author: $route.query.author,
                        category: 'photography',
                        year: $route.query.year
                      }
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      $route.query.category === 'photography' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.photography') }}
                  </router-link>
                </li>
                <li
                  :class="[
                    'nav-item',
                    $route.query.category === 'technology' ? 'active' : null
                  ]"
                >
                  <router-link
                    :to="{
                      name: 'ArticleList',
                      query: {
                        author: $route.query.author,
                        category: 'technology',
                        year: $route.query.year
                      }
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      $route.query.category === 'technology' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.technology') }}
                  </router-link>
                </li>
                <li
                  :class="[
                    'nav-item',
                    $route.query.category === 'wedding' ? 'active' : null
                  ]"
                >
                  <router-link
                    :to="{
                      name: 'ArticleList',
                      query: {
                        author: $route.query.author,
                        category: 'wedding',
                        year: $route.query.year
                      }
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      $route.query.category === 'wedding' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.wedding') }}
                  </router-link>
                </li>
              </ul>
              <hr>
              <h6 class="lead fw-bold">{{ $t('blog.years') }}</h6>
              <ul class="nav nav-pills mb-3">
                <li
                  v-for="yearNumber in getYears()"
                  :class="[
                    'nav-item',
                    $route.query.year == yearNumber ? 'active' : null
                  ]"
                >
                  <router-link
                    :to="{
                      name: 'ArticleList',
                      query: {
                        author: $route.query.author,
                        category: $route.query.category,
                        year: yearNumber
                      }
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      $route.query.year == yearNumber ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ yearNumber }}
                  </router-link>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media(min-width: 992px) {
  #filter_menu {
    position: -webkit-sticky;
    position: sticky;
    top: 125px;
  }
}
</style>
