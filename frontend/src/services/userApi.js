import axios from "axios"
import {computed} from "vue";

const BASE_URL = "http://127.0.0.1:8000/"

export function postLogin(username, password) {
    return axios.post(`${BASE_URL}login/`, {
        username,
        password,
    })
}

export function postRegister(data) {
    return axios.post(`${BASE_URL}register/`, data)
}

export function getProfile() {
    const token = localStorage.getItem('accessToken')
    return axios.get(`${BASE_URL}profile/`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
}

export function postProfiles(data) {
    const token = localStorage.getItem('accessToken')
    return axios.patch(`${BASE_URL}profile/`, data, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
}