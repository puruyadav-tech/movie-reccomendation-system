import pickle, requests, streamlit as st

st.set_page_config(page_title="CineMatch", page_icon="🎬", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #08080a;
    color: #ddd8cc;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── Filmstrip top bar ── */
.filmstrip {
    display: flex;
    align-items: center;
    background: #0f0e10;
    border-bottom: 1px solid #1e1c22;
    padding: 0 1rem;
    height: 36px;
    gap: 6px;
}
.sprocket {
    width: 20px; height: 14px;
    border: 1.5px solid #2a2730;
    border-radius: 3px;
    background: #08080a;
    flex-shrink: 0;
}
.strip-text {
    font-size: 10px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #3d3948;
    flex: 1;
    text-align: center;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3.5rem 4rem 2.5rem;
    position: relative;
    border-bottom: 0.5px solid #1a1820;
    margin-bottom: 2rem;
}
.curtain::before, .curtain::after {
    content: '';
    position: absolute;
    top: 0; bottom: 0;
    width: 56px;
    background: #0c0b0e;
}
.curtain::before { left: 0; border-right: 2px solid #1a1820; }
.curtain::after  { right: 0; border-left:  2px solid #1a1820; }

.tagline {
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7c6f9a;
    margin-bottom: 1rem;
}
.headline {
    font-family: 'Cormorant Garamond', serif;
    font-size: 46px;
    font-weight: 600;
    color: #f2ede4;
    line-height: 1.08;
    margin-bottom: 0.4rem;
}
.headline em { font-style: italic; color: #c4a882; }
.subline {
    font-size: 14px;
    color: #5e5868;
    line-height: 1.7;
    margin-bottom: 0;
}
.subline span { color: #9a8ab0; }

/* ── Select + Button ── */
div[data-baseweb="select"] > div {
    background: #13111a !important;
    border: 0.5px solid #2e2a38 !important;
    border-radius: 8px !important;
    color: #ddd8cc !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}
div[data-baseweb="select"] svg { fill: #6b5f80 !important; }

div.stButton > button {
    background: #c4a882 !important;
    color: #08080a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 8px !important;
    height: 44px !important;
    width: 100% !important;
    transition: background .15s !important;
}
div.stButton > button:hover { background: #d4bc9a !important; }

/* ── Section label ── */
.rh {
    display: flex;
    align-items: baseline;
    gap: 10px;
    margin-bottom: 1.4rem;
}
.rh-label {
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #3d3948;
}
.rh-movie {
    font-family: 'Cormorant Garamond', serif;
    font-size: 20px;
    font-style: italic;
    color: #c4a882;
}

/* ── Cards ── */
.movie-card {
    background: #0f0e14;
    border: 0.5px solid #1e1c26;
    border-radius: 10px;
    overflow: hidden;
    transition: border-color .2s, transform .2s;
    height: 100%;
}
.movie-card:hover {
    border-color: #4a4060;
    transform: translateY(-4px);
}
.poster-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 2/3;
    overflow: hidden;
    background: #13111a;
}
.poster-wrap img {
    width: 100%; height: 100%;
    object-fit: cover; display: block;
}
.no-poster {
    width: 100%; height: 100%;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    color: #2e2a38; font-size: 13px; gap: 8px;
}
.rank-pill {
    position: absolute;
    bottom: 8px; left: 8px;
    background: #c4a882;
    color: #08080a;
    font-family: 'Cormorant Garamond', serif;
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.08em;
    padding: 2px 8px;
    border-radius: 20px;
}
.card-body { padding: 0.65rem 0.8rem 0.8rem; }
.card-name {
    font-size: 13px; font-weight: 500;
    color: #ddd8cc; line-height: 1.35; margin: 0;
}
.card-vibe {
    font-size: 11px; color: #4a4060;
    font-style: italic; margin-top: 4px;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem 3rem;
    color: #3d3948;
}
.empty-state p {
    font-size: 14px; line-height: 1.8;
    max-width: 280px; margin: 0.8rem auto 0;
    color: #4a4060;
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 17px;
}
</style>
""", unsafe_allow_html=True)

# ── Models ────────────────────────────────────────────────────────────────────
movies     = pickle.load(open('Model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('Model/similarity1.pkl', 'rb'))

VIBES = [
    "A mirror, held gently",
    "Darkness with a heartbeat",
    "Time, bending beautifully",
    "A wound that heals watching",
    "Pure adrenaline, distilled",
    "Grief dressed as beauty",
    "The mind at war with itself",
    "Quiet devastation",
    "A fist through the screen",
    "Wonder, uncut",
]
RANKS = ["#1 pick", "#2 pick", "#3 pick", "#4 pick", "#5 pick"]

def fetch_poster(movie_id):
    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        "?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    )
    try:
        path = requests.get(url, timeout=5).json().get('poster_path')
        return f"https://image.tmdb.org/t/p/w342{path}" if path else None
    except Exception:
        return None

# ── Filmstrip ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="filmstrip">
  <div class="sprocket"></div><div class="sprocket"></div><div class="sprocket"></div>
  <div class="strip-text">CineMatch — where every frame leads somewhere new</div>
  <div class="sprocket"></div><div class="sprocket"></div><div class="sprocket"></div>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero curtain">
  <p class="tagline">Your personal projectionist</p>
  <h1 class="headline">Every great film deserves<br>an <em>encore.</em></h1>
  <p class="subline">
    Tell us what moved you.<br>
    We'll find five films that <span>live in the same soul.</span>
  </p>
</div>
""", unsafe_allow_html=True)

# ── Controls ──────────────────────────────────────────────────────────────────
col_sel, col_btn = st.columns([4, 1])
with col_sel:
    selected = st.selectbox("", movies['title'].values, label_visibility="collapsed")
with col_btn:
    go = st.button("Roll the reel")

# ── Results ───────────────────────────────────────────────────────────────────
if go:
    idx       = movies[movies['title'] == selected].index[0]
    distances = sorted(
        enumerate(similarity[idx]), key=lambda x: x[1], reverse=True
    )[1:6]

    st.markdown(
        f'<div class="rh"><span class="rh-label">Because you loved</span>'
        f'<span class="rh-movie">{selected}</span></div>',
        unsafe_allow_html=True
    )

    cols = st.columns(5)
    for i, (col, (movie_idx, score)) in enumerate(zip(cols, distances)):
        title  = movies.iloc[movie_idx].title
        m_id   = movies.iloc[movie_idx].movie_id
        poster = fetch_poster(m_id)
        vibe   = VIBES[(i + idx) % len(VIBES)]

        poster_html = (
            f'<img src="{poster}" alt="{title}">'
            if poster else
            '<div class="no-poster">No poster</div>'
        )

        with col:
            st.markdown(f"""
            <div class="movie-card">
              <div class="poster-wrap">
                {poster_html}
                <span class="rank-pill">{RANKS[i]}</span>
              </div>
              <div class="card-body">
                <p class="card-name">{title}</p>
                <p class="card-vibe">{vibe}</p>
              </div>
            </div>
            """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty-state">
      <p>"Choose a film above. The lights will dim,<br>and five kindred stories will find you."</p>
    </div>
    """, unsafe_allow_html=True)
