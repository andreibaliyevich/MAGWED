import axios from 'axios'

export function useLogout() {

  const logout = () => {
    axios.post('/accounts/auth/logout/')
    .then(() => {
      window.localStorage.removeItem('user')
      window.location.reload()
    })
  }

  return logout
}
