import axios from 'axios'
import { useAuthStore } from '../store/authStore'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth endpoints
export const authAPI = {
  register: (data: {
    username: string
    email: string
    password: string
    phone: string
    age: number
    gender: string
  }) => api.post('/user/reg', data),
  login: (username: string, password: string) =>
    api.post('/user/log', { username, password }),
  getProfile: () => api.get('/user/my_profile'),
}

// Posts endpoints
export const postsAPI = {
  getAllPosts: () => api.get('/post/posts'),
  createPost: (content: string) =>
    api.post('/post/new_post', { content }),
  getPost: (postId: string) => api.get(`/post/${postId}`),
  editPost: (postId: string, content: string) =>
    api.put('/post/edit', { post_id: postId, content }),
  deletePost: (postId: string) => api.delete(`/post/del/${postId}`),
  favoritePost: (postId: string) =>
    api.post(`/post/${postId}/favorite`),
}

// Comments endpoints
export const commentsAPI = {
  getComments: (postId: string) =>
    api.get(`/posts/comment/${postId}`),
  createComment: (postId: string, content: string) =>
    api.post(`/posts/comment/${postId}`, { content }),
  editComment: (commentId: string, content: string) =>
    api.put(`/posts/comment/${commentId}`, { content }),
  deleteComment: (commentId: string) =>
    api.delete(`/posts/comment/${commentId}`),
  likeComment: (commentId: string) =>
    api.post(`/posts/comment/${commentId}/like`),
}

// User endpoints
export const usersAPI = {
  getUser: (userId: string) => api.get(`/user/profile/${userId}`),
  follow: (userId: string) => api.post(`/follow/${userId}`),
  getFollowers: (userId: string) =>
    api.get(`/followers/${userId}`),
  getFollowing: (userId: string) =>
    api.get(`/user/my_profile/following`),
  editProfile: (data: any) => api.put('/user/my_profile/edit', data),
}

// Search endpoints
export const searchAPI = {
  searchPosts: (query: string) =>
    api.get('/search/post', { params: { q: query } }),
  searchUsers: (query: string) =>
    api.get('/search/user', { params: { q: query } }),
}

export default api
