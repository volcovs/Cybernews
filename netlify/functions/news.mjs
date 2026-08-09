import { Dropbox } from "dropbox";

const dbx = new Dropbox({
    clientId: process.env.DROPBOX_APP_KEY,
    clientSecret: process.env.DROPBOX_APP_SECRET,
    refreshToken: process.env.DROPBOX_REFRESH_TOKEN,
});

function normalizePath(path) {
    path = path.replaceAll("\\", "/").trim();

    if (!path) {
        throw new Error("Dropbox path cannot be empty");
    }

    if (!path.startsWith("/")) {
        path = "/" + path;
    }

    while (path.includes("//")) {
        path = path.replaceAll("//", "/");
    }

    return path;
}

async function readText(path) {
    const response = await dbx.filesDownload({
        path: normalizePath(path),
    });

    const result = response.result;

    if (typeof result.fileBinary === "string") {
        return Buffer
            .from(result.fileBinary, "base64")
            .toString("utf-8");
    }

    if (result.fileBlob) {
        return await result.fileBlob.text();
    }

    throw new Error("Unable to read Dropbox file");
}

export default async () => {
    try {
        const result = await dbx.filesListFolder({
            path: normalizePath(
                process.env.DROPBOX_ROOT || ""
            ),
        });

        const articles = [];

        for (const entry of result.result.entries) {
            if (
                entry[".tag"] !== "file" ||
                !entry.name.endsWith(".jsonl")
            ) {
                continue;
            }

            const content = await readText(entry.path_lower);

            for (const line of content.split("\n")) {
                if (!line.trim()) {
                    continue;
                }

                articles.push(
                    JSON.parse(line)
                );
            }
        }

        articles.sort(
            (a, b) =>
                new Date(b.published_at || b.fetched_at) -
                new Date(a.published_at || a.fetched_at)
        );

        return new Response(
            JSON.stringify({
                articles,
            }),
            {
                status: 200,
                headers: {
                    "Content-Type": "application/json",
                    "Cache-Control":
                        "public, max-age=300",
                },
            }
        );
   } catch (error) {
        console.error("Dropbox/API error:", error);

        return new Response(
            JSON.stringify({
                error: "Failed to retrieve news",
                message: error?.message || String(error),
                name: error?.name || "UnknownError",
            }),
            {
                status: 500,
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );
    }
};