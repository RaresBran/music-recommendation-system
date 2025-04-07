<template>
  <div class="DaoRb">
    <h1 class="eSHwvX">Create an account</h1>
    <form @submit.prevent="signUp">
      <ErrorAlert :error-msg="authError" @clearError="clearError" />
      <div class="jGQTZC">
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="text" placeholder="First name" v-model="name" />
          </div>
        </label>
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="text" placeholder="Last name" v-model="lastname" />
          </div>
        </label>
        <label class="iJLvzO">
          <div class="fdCSlG">
            <select multiple class="cmCuLh" v-model="selectedGenres">
              <option value="" disabled>Select music genres</option>
              <option v-for="genre in musicGenres" :key="genre" :value="genre">
                {{ genre }}
              </option>
            </select>
          </div>
        </label>
        <label class="iJLvzO">
          <div class="fdCSlG">
            <select multiple class="cmCuLh" v-model="selectedArtists">
              <option value="" disabled>Select favorite artists</option>
              <option v-for="artist in artists" :key="artist" :value="artist">
                {{ artist }}
              </option>
            </select>
          </div>
        </label>
        <label class="iJLvzO">
          <div class="fdCSlG">
            <select multiple class="cmCuLh" v-model="selectedYears">
              <option value="" disabled>Select release years</option>
              <option v-for="year in releaseYears" :key="year" :value="year">
                {{ year }}
              </option>
            </select>
          </div>
        </label>
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="text" placeholder="Email address" v-model="email" />
          </div>
        </label>
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="password" placeholder="Password" v-model="password" />
          </div>
        </label>
      </div>
      <div class="jGQTZC">
        <button class="gZMQdu" type="submit" :disabled="loading">
          <div class="bjhGPG" :class="{loading: loading}">Sign up</div>
          <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="jjoFVh" :class="{loading: loading}">
            <g fill="none" stroke-width="1.5" stroke-linecap="round" class="faEWLr" style="stroke: var(--icon-color);">
              <circle stroke-opacity=".2" cx="8" cy="8" r="6"></circle>
              <circle cx="8" cy="8" r="6" class="VFMrX"></circle>
            </g>
          </svg>
        </button>
        <div class="xxEKN">
          By signing up you agree to our
          <a href="https://policies.google.com/terms" target="_blank" rel="noopener noreferrer" class="bkFclS">
            <span>API Terms of Service</span>
          </a>
          and
          <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer" class="bkFclS">
            <span>Privacy Policy</span>
          </a>.
        </div>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
// Previous imports and page meta remain the same
definePageMeta({
  layout: "auth"
})
useHead({
  title: 'Register | supaAuth'
})
// Form fields
const email = ref('')
const password = ref('')
const name = ref('')
const lastname = ref('')
const selectedGenres = ref<string[]>([])
const selectedArtists = ref<string[]>([])
const selectedYears = ref<string[]>([])

// Options arrays remain the same
const musicGenres = [
  'Rock', 'Pop', 'Hip Hop', 'Jazz', 'Classical', 'Electronic',
  'R&B', 'Country', 'Blues', 'Folk', 'Metal', 'Indie'
]
const artists = [
  'The Beatles', 'Queen', 'Michael Jackson', 'Taylor Swift',
  'Ed Sheeran', 'Drake', 'Beyoncé', 'Adele', 'Lady Gaga',
  'Eminem', 'Coldplay', 'Bruno Mars'
]
const currentYear = new Date().getFullYear()
const releaseYears = Array.from(
  { length: currentYear - 1959 },
  (_, i) => (currentYear - i).toString()
)

const client = useSupabaseAuthClient()
const user = useSupabaseUser()
const loading = ref(false)
const authError = ref('')

watchEffect(async () => {
  if (user.value) {
    await navigateTo('/')
  }
})

const insertUserPreferences = async (userId: string) => {
  const { error } = await client
    .from('user_preferences')
    .insert({
      user_id: userId,
      music_genres: selectedGenres.value,
      favorite_artists: selectedArtists.value,
      preferred_years: selectedYears.value
    })

  if (error) {
    console.error('Error inserting preferences:', error)
    throw error
  }
}

const signUp = async () => {
  try {
    // Validation
    if (!name.value) return authError.value = 'First name required'
    if (!lastname.value) return authError.value = 'Last name required'
    if (selectedGenres.value.length === 0) return authError.value = 'Please select at least one music genre'
    if (!email.value) return authError.value = 'Email required'
    if (!password.value) return authError.value = 'Password required'
    
    loading.value = true

    // Register the user
    const { data: authData, error: authError } = await client.auth.signUp({
      email: email.value,
      password: password.value,
      options: {
        data: {
          first_name: name.value,
          last_name: lastname.value
        }
      }
    })

    if (authError) throw authError

    // If registration successful, insert preferences
    if (authData.user) {
      await insertUserPreferences(authData.user.id)
      // You might want to show a success message here
      await navigateTo('/')
    }
  } catch (error) {
    console.error('Signup error:', error)
    authError.value = error.message || 'An error occurred during signup'
  } finally {
    loading.value = false
  }
}

const clearError = () => {
  authError.value = ''
}
</script>

