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
          <RouterView />
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
                    this.$route.query.category == 'design' ? 'active' : null
                  ]"
                >
                  <LocaleRouterLink
                    routeName="ArticleList"
                    :routeQuery="{
                      author: this.$route.query.author,
                      category: 'design',
                      year: this.$route.query.year
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      this.$route.query.category == 'design' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.design') }}
                  </LocaleRouterLink>
                </li>
                <li
                  :class="[
                    'nav-item',
                    this.$route.query.category == 'fashion' ? 'active' : null
                  ]"
                >
                  <LocaleRouterLink
                    routeName="ArticleList"
                    :routeQuery="{
                      author: this.$route.query.author,
                      category: 'fashion',
                      year: this.$route.query.year
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      this.$route.query.category == 'fashion' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.fashion') }}
                  </LocaleRouterLink>
                </li>
                <li
                  :class="[
                    'nav-item',
                    this.$route.query.category == 'inspiration' ? 'active' : null
                  ]"
                >
                  <LocaleRouterLink
                    routeName="ArticleList"
                    :routeQuery="{
                      author: this.$route.query.author,
                      category: 'inspiration',
                      year: this.$route.query.year
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      this.$route.query.category == 'inspiration' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.inspiration') }}
                  </LocaleRouterLink>
                </li>
                <li
                  :class="[
                    'nav-item',
                    this.$route.query.category == 'journey' ? 'active' : null
                  ]"
                >
                  <LocaleRouterLink
                    routeName="ArticleList"
                    :routeQuery="{
                      author: this.$route.query.author,
                      category: 'journey',
                      year: this.$route.query.year
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      this.$route.query.category == 'journey' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.journey') }}
                  </LocaleRouterLink>
                </li>
                <li
                  :class="[
                    'nav-item',
                    this.$route.query.category == 'lifestyle' ? 'active' : null
                  ]"
                >
                  <LocaleRouterLink
                    routeName="ArticleList"
                    :routeQuery="{
                      author: this.$route.query.author,
                      category: 'lifestyle',
                      year: this.$route.query.year
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      this.$route.query.category == 'lifestyle' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.lifestyle') }}
                  </LocaleRouterLink>
                </li>
                <li
                  :class="[
                    'nav-item',
                    this.$route.query.category == 'photography' ? 'active' : null
                  ]"
                >
                  <LocaleRouterLink
                    routeName="ArticleList"
                    :routeQuery="{
                      author: this.$route.query.author,
                      category: 'photography',
                      year: this.$route.query.year
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      this.$route.query.category == 'photography' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.photography') }}
                  </LocaleRouterLink>
                </li>
                <li
                  :class="[
                    'nav-item',
                    this.$route.query.category == 'technology' ? 'active' : null
                  ]"
                >
                  <LocaleRouterLink
                    routeName="ArticleList"
                    :routeQuery="{
                      author: this.$route.query.author,
                      category: 'technology',
                      year: this.$route.query.year
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      this.$route.query.category == 'technology' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.technology') }}
                  </LocaleRouterLink>
                </li>
                <li
                  :class="[
                    'nav-item',
                    this.$route.query.category == 'wedding' ? 'active' : null
                  ]"
                >
                  <LocaleRouterLink
                    routeName="ArticleList"
                    :routeQuery="{
                      author: this.$route.query.author,
                      category: 'wedding',
                      year: this.$route.query.year
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      this.$route.query.category == 'wedding' ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ $t('category_choices.wedding') }}
                  </LocaleRouterLink>
                </li>
              </ul>
              <hr>
              <h6 class="lead fw-bold">{{ $t('blog.years') }}</h6>
              <ul class="nav nav-pills mb-3">
                <li
                  v-for="yearNumber in getYears()"
                  :class="[
                    'nav-item',
                    this.$route.query.year == yearNumber ? 'active' : null
                  ]"
                >
                  <LocaleRouterLink
                    routeName="ArticleList"
                    :routeQuery="{
                      author: this.$route.query.author,
                      category: this.$route.query.category,
                      year: yearNumber
                    }"
                    @click="$refs.filterMenuClose.click()"
                    :class="[
                      'nav-link',
                      this.$route.query.year == yearNumber ? 'active' : 'text-dark'
                    ]"
                  >
                    {{ yearNumber }}
                  </LocaleRouterLink>
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
