import axios from 'axios'

export function createProject(data) {
    const token = localStorage.getItem('accessToken')
    return axios.post('http://localhost:8000/api/projects/', data, {
        headers: {Authorization: `Bearer ${token}`}
    })
}

export function fetchProjectsByTeam(teamId) {
    const token = localStorage.getItem('accessToken')
    return axios.get(`http://localhost:8000/api/projects/?team=${teamId}`, {
        headers: {Authorization: `Bearer ${token}`}
    })
}

export function fetchMyTeamsWithProjects() {
    const token = localStorage.getItem('accessToken')
    return axios.get('http://localhost:8000/api/my-teams-with-projects/', {
        headers: {Authorization: `Bearer ${token}`}
    })
}

export function fetchProjectDetail(projectId) {
    const token = localStorage.getItem('accessToken')
    return axios.get(`/api/projects/${projectId}/`, {
        headers: {Authorization: `Bearer ${token}`}
    })
}

export function fetchMyProjects() {
    const token = localStorage.getItem('accessToken')
    return axios.get('http://localhost:8000/api/projects/', {
        headers: {Authorization: `Bearer ${token}`}
    })
}

export function updateProject(projectId, data) {
    const token = localStorage.getItem('accessToken')
    return axios.patch(`http://localhost:8000/api/projects/${projectId}/`, data, {
        headers: {Authorization: `Bearer ${token}`}
    })
}

export async function teamMembers(projectId) {
    const token = localStorage.getItem('accessToken')
    return await axios.get(`http://localhost:8000/api/projects/${projectId}/assignable-users`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
}