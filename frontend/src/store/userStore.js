import {defineStore} from 'pinia'
import {getProfile} from "../services/userApi.js";

export const useUserStore = defineStore('user', {
    state: () => ({
        accessToken: localStorage.getItem('accessToken'),
        refreshToken: localStorage.getItem('refreshToken'),
        user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null
    }),
    actions: {
        async login(access, refresh) {
            this.accessToken = access
            this.refreshToken = refresh
            localStorage.setItem('accessToken', access)
            localStorage.setItem('refreshToken', refresh)
            await this.loadUser() // girişte otomatik profil çek
            if (this.user) {
                localStorage.setItem('user', JSON.stringify(this.user))
            }
        },
        async logout() {
            this.accessToken = null
            this.refreshToken = null
            this.user = null
            localStorage.removeItem('accessToken')
            localStorage.removeItem('refreshToken')
            localStorage.removeItem('user')
        },
        async loadUser() {
            if (!this.accessToken) {
                console.log("No accessToken")
                return
            }
            try {
                const res = await getProfile() // API'den profil çek
                this.user = res.data
                localStorage.setItem('user', JSON.stringify(this.user))
            } catch (e) {
                console.log("Failed to load user")
                this.user = null
                localStorage.removeItem('user')
            }
        }
    }
})
