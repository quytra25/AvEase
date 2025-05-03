import axios from 'axios'

// Setup CSRF token for Django
axios.defaults.withCredentials = true
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

const api = axios.create({
baseURL: 'http://localhost:8000/api/',
withCredentials: true,
headers: {
    'Content-Type': 'application/json'
}
})

export default {
// CSRF
getCsrfToken() {
    return api.get('csrf/')
},

// Events
listEvents() {
    return api.get('events/')
},
createEvent(data) {
    return api.post('events/', data)
},
getEvent(id) {
    return api.get(`events/${id}/`)
},
updateEvent(id, data) {
    return api.patch(`events/${id}/`, data)
},

// Participants
joinEvent(eventID) {
    return api.post('participants/', { event: eventID })
},
joinEventAsGuest(eventID, payload) {
    return api.post('participants/guest/', {
    event: eventID,
    guest_name: payload.guest_name
    })
},

// Availabilities
addAvailability(payload) {
    return api.post('availabilities/', payload)
}
}