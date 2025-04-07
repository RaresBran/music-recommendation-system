<template>
  <div class="relative z-10 max-w-screen">
    <div class="flex items-center justify-between">
      <!-- Info Section (Left) -->
      <div class="w-1/3">
        <p v-if="user" class="fVeafc in">Hi {{ user.user_metadata.first_name }}</p>
        <p v-else class="fVeafc">Discover your music matches</p>
        <h1 class="kKxhrq">
          Matches
          <br>
          Find your music soulmates
        </h1>
        <p class="kRTmDC">
          Based on your preferences, here are some music matches that you might enjoy.
        </p>
      </div>
      <!-- Song Card (Right) -->
      <div v-if="user && currentSong" class="w-2/3 pl-8">
        <iframe style="border-radius:12px"
          :src="`https://open.spotify.com/embed/track/${currentSong.id}?utm_source=generator`" width="100%" height="352"
          frameborder="0" allowfullscreen="true"
          allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>

        <div class="flex justify-center">
          <button @click="likeSong" class="like-button w-1/2">❤️ Like</button>
          <button @click="dislikeSong" class="dislike-button w-1/2">💔 Dislike</button>
          <!-- Add this button next to your existing like button -->
          <button @click="handleFavorite" class="favorite-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"
                :fill="isFavorite ? '#FFD700' : 'none'" stroke="currentColor" stroke-width="2" />
            </svg>
          </button>
        </div>

      </div>
    </div>

    <!-- Add this after your existing song card div -->
    <div class="mt-8 w-full">
      <button @click="toggleFavorites" class="mb-4 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
        {{ showFavorites ? 'Hide Favorites' : 'Show Favorites' }}
      </button>
    </div>

    <!-- Navigation buttons -->
    <div class="uQxNj" v-if="user">
      <NuxtLink to="/">
        <button class="ieMfVH">
          <span class="fKlELC">Back to Home</span>
        </button>
      </NuxtLink>
    </div>
    <div class="uQxNj" v-else>
      <NuxtLink class="bQRHNT" to="/login">
        <span class="fKlELC">
          Login
          <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="taKtSf">
            <path class="chevron" d="M8 13L13 8L8 3" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="round">
            </path>
            <path class="stem" d="M12 8L2 8" stroke-width="1.5"></path>
          </svg>
        </span>
      </NuxtLink>
      <NuxtLink to="/register">
        <button class="ieMfVH">
          <span class="fKlELC">Sign up</span>
        </button>
      </NuxtLink>
    </div>
  </div>

  <!-- Favorites Sidebar -->
  <Transition name="overlay">
    <div v-if="showFavorites" 
         class="fixed inset-0 bg-black bg-opacity-50 z-40"
         @click="toggleFavorites">
    </div>
  </Transition>

  <Transition name="slide">
    <div v-if="showFavorites" 
         class="fixed right-0 top-0 h-full w-96 bg-white shadow-lg z-50 overflow-y-auto">
      <div class="p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold">Favorites</h2>
          <button @click="toggleFavorites" 
                  class="p-2 hover:bg-gray-100 rounded-full">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="space-y-4">
          <div v-for="song in favoritedSongs" 
               :key="song.spotify_id" 
               class="favorite-card bg-gray-50 rounded-lg p-4">
            <iframe 
              style="border-radius:12px"
              :src="`https://open.spotify.com/embed/track/${song.spotify_id}?utm_source=generator`" 
              width="100%" 
              height="152" 
              frameborder="0" 
              allowfullscreen="true"
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
              loading="lazy">
            </iframe>
            <button @click="removeFavorite(song.id)"
                    class="mt-2 w-full px-4 py-2 text-red-600 border border-red-600 rounded-lg hover:bg-red-50">
              Remove from Favorites
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { GoogleGenerativeAIEmbeddings } from "@langchain/google-genai";
import { TaskType } from "@google/generative-ai";

const supabase = useSupabaseAuthClient()
const user = useSupabaseUser()
const router = useRouter()


const embeddings = new GoogleGenerativeAIEmbeddings({
  model: "text-embedding-004", // 768 dimensions
  taskType: TaskType.RETRIEVAL_DOCUMENT,
  apiKey: "",
  title: "Document title",
});

if (!user) {
  router.push('/login')
}

useHead({
  title: 'Matches',
  meta: [
    { name: 'description', content: 'Discover your music matches based on your preferences.' }
  ]
})

const currentSong = ref(null)
const isFavorite = ref(false)
const showFavorites = ref(false)
const favoritedSongs = ref([])

const fetchSong = async () => {
  await updateRecommendations()
  
  // Reset favorite state for new song
  isFavorite.value = false
  
  // Check if new song is already in favorites
  if (currentSong.value) {
    const { data: favoriteCheck } = await supabase
      .from('favorites')
      .select()
      .eq('user_id', user.value.id)
      .eq('song_id', currentSong.value.id_db)
      .single()
    
    isFavorite.value = !!favoriteCheck
  }
}

const likeSong = async () => {
  if (!currentSong.value) return
  console.log(user)
  const { data, error } = await supabase.from('likes').insert({
    user_id: user.value.id,
    song_id: currentSong.value.id_db,
  })
  if (error) {
    console.error(error)
  } else {
    fetchSong()
  }
}

const dislikeSong = async () => {
  if (!currentSong.value) return
  console.log(user)
  console.log(currentSong)
  const { data, error } = await supabase.from('dislikes').insert({
    user_id: user.value.id,
    song_id: currentSong.value.id_db,

  })
  if (error) {
    console.error(error)
  } else {
    fetchSong()
  }
}

async function handleFavorite() {
  try {
    if (!user.value || !currentSong.value) return

    if (isFavorite.value) {
      const { error } = await supabase
        .from('favorites')
        .delete()
        .eq('user_id', user.value.id)
        .eq('song_id', currentSong.value.id_db)

      if (!error) {
        isFavorite.value = false
      }
    } else {
      const songData = {
        user_id: user.value.id,
        song_id: currentSong.value.id_db,
        spotify_id: currentSong.value.id,
        favorited_at: new Date()
      }

      const { error } = await supabase
        .from('favorites')
        .upsert(songData)

      if (!error) {
        isFavorite.value = true
      }
    }
  } catch (error) {
    console.error('Error handling favorite:', error)
  }
}

const toggleFavorites = async () => {
  showFavorites.value = !showFavorites.value
  if (showFavorites.value) {
    const { data, error } = await supabase
      .from('favorites')
      .select('id, song_id, spotify_id')
      .eq('user_id', user.value.id)

    if (error) {
      console.error('Error fetching favorites:', error)
    } else {
      favoritedSongs.value = data.map(fav => ({
        spotify_id: fav.spotify_id
        
      }))
    }
  }
}

const removeFavorite = async (songId) => {
  try {
    const { error } = await supabase
      .from('favorites')
      .delete()
      .eq('user_id', user.value.id)
      .eq('song_id', songId)

    if (error) throw error

    favoritedSongs.value = favoritedSongs.value.filter(song => song.id !== songId)
  } catch (error) {
    console.error('Error removing favorite:', error)
  }
}

async function getLikedSongs() {
  const { data: likedSongs, error } = await supabase
    .from('likes')
    .select('song_id')
    .eq('user_id', user.value.id)
  
  if (error) throw error
  return likedSongs
}

async function getFavoriteSongs() {
  const { data: favoriteSongs, error } = await supabase
    .from('favorites')
    .select('song_id')
    .eq('user_id', user.value.id)
  
  if (error) throw error
  return favoriteSongs
}

async function generateSongEmbedding(songFeatures) {
  // Combine relevant features into a string
  // combine everything from the song object into a single string appart from the id and id_db and embeddings
  const songText = Object.values(songFeatures)
    .filter(val => typeof val === 'string')
    .join(' ')
  
  return await embeddings.embedQuery(songText)
}

async function findSimilarSongs(embedding) {
  const { data: similarSongs, error } = await supabase.rpc('match_songs', {
    query_embedding: embedding,
    match_threshold: 0.2,
    match_count: 5,
    current_user_id: user.value.id  // Add this parameter
  })
  
  if (error) throw error
  return similarSongs
}

async function updateRecommendations() {
  try {
    // Get user's liked and favorite songs
    const likedSongs = await getLikedSongs()
    const favoriteSongs = await getFavoriteSongs()
    
    // If no liked or favorite songs, use backup recommendations
    if ((!likedSongs || likedSongs.length === 0) && (!favoriteSongs || favoriteSongs.length === 0)) {
      const { data, error } = await supabase.from('songs').select('*')
      if (error) {
        console.error(error)
      } else {
        currentSong.value = data[Math.floor(Math.random() * data.length)]
      }
      return
    }

    // Generate embeddings for liked and favorite songs
    const likedEmbeddings = await Promise.all(
      likedSongs.map(song => generateSongEmbedding(song))
    )
    const favoriteEmbeddings = await Promise.all(
      favoriteSongs.map(song => generateSongEmbedding(song))
    )

    // Combine embeddings with double margin for favorites
    const combinedEmbeddings = likedEmbeddings.concat(favoriteEmbeddings, favoriteEmbeddings)
    const averageEmbedding = averageVectors(combinedEmbeddings)
    const recommendations = await findSimilarSongs(averageEmbedding)
    
    console.log('Recommendations:', recommendations)

    currentSong.value = recommendations[0]

  } catch (error) {
    console.error('Error updating recommendations:', error)
    // Fallback to backup recommendations on error
    const { data: backUpRecommendations } = await supabase
      .from('songs')
      .select('id, id_db')
      .limit(5)
    
    currentSong.value = backUpRecommendations[0]
  }
}

// Helper to average embedding vectors
function averageVectors(vectors) {
  const sum = vectors.reduce((acc, curr) => {
    return acc.map((val, idx) => val + curr[idx])
  })
  return sum.map(val => val / vectors.length)
}



onMounted(fetchSong)
</script>

<style>
.song-card {
  border: 1px solid #ccc;
  padding: 16px;
  margin: 16px 0;
}

.like-button,
.dislike-button {
  margin: 8px;
}

.like-button,
.dislike-button {
  margin: 8px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.like-button {
  background: linear-gradient(90deg, #ff7eb3, #ff758c);
  color: white;
}

.dislike-button {
  background: linear-gradient(90deg, #808080, #4a4a4a);
  color: white;
}

.like-button:hover,
.dislike-button:hover {
  transform: translateY(-3px);
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.like-button:active,
.dislike-button:active {
  transform: translateY(1px);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.favorite-btn {
  padding: 8px;
  background: transparent;
  border: none;
  cursor: pointer;
  color: currentColor;
  transition: transform 0.2s;
}

.favorite-btn:hover {
  transform: scale(1.1);
}

.overlay-enter-active,
.overlay-leave-active {
  transition: opacity 0.3s ease;
}

.overlay-enter-from,
.overlay-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}

.favorite-card {
  transition: transform 0.2s ease;
}

.favorite-card:hover {
  transform: translateY(-2px);
}
</style>