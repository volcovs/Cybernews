export default async () => {
    return new Response(
        JSON.stringify({
            status: "ok",
            message: "CyberNews API is alive"
        }),
        {
            headers: {
                "Content-Type": "application/json"
            }
        }
    );
};