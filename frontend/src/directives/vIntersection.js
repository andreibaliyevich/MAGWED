export default {
  name: 'intersection',

  mounted(el, binding) {
    const options = {
      root: binding.value.scrollArea,
      rootMargin: '0px',
      threshold: 1.0
    }
    const callback = (entries, observer) => {
      if (entries[0].isIntersecting) {
        binding.value.callbackFunction(...binding.value.functionArguments)
      }
    }
    const observer = new IntersectionObserver(callback, options)
    observer.observe(el)
  }
}
