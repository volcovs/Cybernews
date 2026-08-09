const articlesContainer =
    document.getElementById("articles");

const loadingElement =
    document.getElementById("loading");

const errorElement =
    document.getElementById("error");

const countElement =
    document.getElementById("article-count");

const categoryFilter =
    document.getElementById("category-filter");

const refreshButton =
    document.getElementById("refresh-button");


let articles = [];


async function loadNews() {
    showLoading();

    try {
        const response = await fetch("/api/news");

        if (!response.ok) {
            throw new Error(
                `API returned ${response.status}`
            );
        }

        const data = await response.json();

        articles = data.articles || [];

        renderArticles();

    } catch (error) {
        console.error(error);

        showError(
            "Unable to load cybersecurity news."
        );
    } finally {
        loadingElement.classList.add("hidden");
    }
}


function renderArticles() {
    const selectedCategory =
        categoryFilter.value;

    let filtered = articles;

    if (selectedCategory !== "all") {
        filtered = articles.filter(
            article =>
                article.category === selectedCategory
        );
    }

    filtered.sort((a, b) => {
        const scoreA =
            a.importance_score ?? 0;

        const scoreB =
            b.importance_score ?? 0;

        if (scoreA !== scoreB) {
            return scoreB - scoreA;
        }

        const dateA = new Date(
            a.published_at || a.fetched_at
        );

        const dateB = new Date(
            b.published_at || b.fetched_at
        );

        return dateB - dateA;
    });

    countElement.textContent =
        `${filtered.length} articles`;

    articlesContainer.innerHTML = "";

    if (filtered.length === 0) {
        articlesContainer.innerHTML = `
            <div class="empty">
                No articles found.
            </div>
        `;

        return;
    }

    for (const article of filtered) {
        articlesContainer.appendChild(
            createArticleCard(article)
        );
    }
}


function createArticleCard(article) {
    const card =
        document.createElement("article");

    card.className = "article-card";

    const score =
        Math.round(article.importance_score ?? 0);

    const category =
        formatCategory(article.category);

    const date =
        formatDate(
            article.published_at ||
            article.fetched_at
        );

    const cves =
        article.cves || [];

    card.innerHTML = `
        <div class="article-header">
            <span class="score">
                ${score}
            </span>

            <div class="article-meta">
                <span class="category">
                    ${escapeHtml(category)}
                </span>

                <span>
                    ${escapeHtml(article.source)}
                </span>

                <span>
                    ${escapeHtml(date)}
                </span>
            </div>
        </div>

        <h3>
            <a
                href="${escapeAttribute(article.url)}"
                target="_blank"
                rel="noopener noreferrer"
            >
                ${escapeHtml(article.title)}
            </a>
        </h3>

        ${
            article.summary
                ? `
                    <p class="summary">
                        ${escapeHtml(
                            article.summary
                        )}
                    </p>
                  `
                : ""
        }

        ${
            cves.length
                ? `
                    <div class="cves">
                        ${cves.map(
                            cve => `
                                <span class="cve">
                                    ${escapeHtml(cve)}
                                </span>
                            `
                        ).join("")}
                    </div>
                  `
                : ""
        }
    `;

    return card;
}


function formatCategory(category) {
    if (!category) {
        return "Other";
    }

    return category
        .replaceAll("_", " ")
        .replace(
            /\b\w/g,
            character => character.toUpperCase()
        );
}


function formatDate(value) {
    if (!value) {
        return "Unknown date";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return "Unknown date";
    }

    return new Intl.DateTimeFormat(
        undefined,
        {
            dateStyle: "medium",
            timeStyle: "short",
        }
    ).format(date);
}


function escapeHtml(value) {
    const div =
        document.createElement("div");

    div.textContent =
        String(value ?? "");

    return div.innerHTML;
}


function escapeAttribute(value) {
    return escapeHtml(value)
        .replaceAll('"', "&quot;");
}


function showLoading() {
    loadingElement.classList.remove(
        "hidden"
    );

    errorElement.classList.add(
        "hidden"
    );
}


function showError(message) {
    loadingElement.classList.add(
        "hidden"
    );

    errorElement.textContent =
        message;

    errorElement.classList.remove(
        "hidden"
    );
}


categoryFilter.addEventListener(
    "change",
    renderArticles
);


refreshButton.addEventListener(
    "click",
    loadNews
);


loadNews();