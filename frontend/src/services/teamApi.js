import axios from 'axios';
const BASE_URL = 'http://localhost:8000/api/teams/';


export async function fetchTeams() {
    const token = localStorage.getItem('accessToken');
    const headers = {'Authorization': `Bearer ${token}`};
    return await axios.get(BASE_URL, {headers});
}

export function fetchTeamDetail(teamId) {
    const token = localStorage.getItem('accessToken');
    const headers = {'Authorization': `Bearer ${token}`};
    return axios.get(`${BASE_URL}${teamId}/`, {headers});
}

export function createTeam(data) {
    const token = localStorage.getItem('accessToken');
    const headers = {'Authorization': `Bearer ${token}`};
    return axios.post(BASE_URL, data, {headers});
}

export function addTeamMember(teamId, userId) {
    const token = localStorage.getItem('accessToken');
    const headers = {'Authorization': `Bearer ${token}`};
    return axios.post(`${BASE_URL}${teamId}/add_member/`, {user_id: userId}, {headers});
}

export function removeTeamMember(teamId, userId) {
    const token = localStorage.getItem('accessToken');
    const headers = {'Authorization': `Bearer ${token}`};
    return axios.post(`${BASE_URL}${teamId}/remove_member/`, {user_id: userId}, {headers});
}

export function getUsers() {
    const token = localStorage.getItem('accessToken');
    const headers = {'Authorization': `Bearer ${token}`};
    return axios.get('http://localhost:8000/users/', {headers});
}
