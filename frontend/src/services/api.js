import axios from 'axios';

// Enable sending cookies with requests
axios.defaults.withCredentials = true;

const api = axios.create({
    baseURL: 'http://localhost:8000/api/',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Utility to get CSRF token from cookie
function getCsrfTokenFromCookie() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
}

// Interceptor to attach CSRF token automatically
api.interceptors.request.use(config => {
    const csrfToken = getCsrfTokenFromCookie();
    if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
});

export default {
  // CSRF
  getCsrfToken() {
    return api.get('csrf/');
  },

  // Events
  listEvents() {
    return api.get('events/');
  },
  createEvent(data) {
    return api.post('events/', data);
  },
  getEvent(link) {
    return api.get(`events/${link}/`);
  },
  getMyEvents() {
    return api.get('my-events/');
  },
  updateEvent(id, data) {
    return api.patch(`events/${id}/`, data);
  },
  deleteEvent(id) {
    return api.delete(`${id}`)
  },
  // Participants
  joinEvent(eventID) {
    return api.post('participants/', { event: eventID });
  },

  joinEventAsGuest(eventID, payload) {
    const csrfToken = getCsrfTokenFromCookie();
    return axios.post(
      'http://localhost:8000/api/participants/guest/',
      {
        event: eventID,
        guest_name: payload.guest_name,
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        withCredentials: true,
      }
    );
  },

  // Availabilities
  addWeeklyAvailability(payload) {
    return api.post('weekly-availabilities/', payload);
  },
  deleteWeeklyAvailability(payload) {
    return api.delete('weekly-availabilities/remove/', {
        data: payload
    });
  },
  getEventAvailabilities(link) {
    return api.get(`events/${link}/availabilities/`);
  },
  addDateAvailability(payload) {
    return api.post('date-availabilities/', payload);
  },
  deleteDateAvailabilities(payload) {
    return api.delete('date-availabilities/remove/', {
        data: payload
    });
  },  
  addRsvpStatus(payload) {
    return api.post('rsvp-statuses/', payload);
  },
  
  // Login/Sign-up
  login(payload) {
    return api.post('login/', payload)
  },

  signup(payload) {
    return api.post('signup/', payload)
  },

  logout() {
    return api.get('logout/')
  },

  getCurrentUser() {
    return api.get('current-user/')
  },

  axios: api // Export axios instance for raw usage
};


  