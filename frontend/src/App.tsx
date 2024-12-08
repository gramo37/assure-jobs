import React, { useState } from "react";
import axios from "axios";

// const URL = "http://66.29.133.117:8000/automate"
const URL = "http://localhost:8000/automate"

const App = () => {
  const [url, setUrl] = useState<string>("");
  const [path, setPath] = useState<string>("");
  const [cookieString, setCookieString] = useState<string>("");
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Make the API call
      const result = await axios.post(URL, {
        url,
        path,
        cookie_string: cookieString,
      });

      console.log(result)
      setResponse(result.data); // Assuming server sends a response
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      setResponse("Error occurred while making the API call.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl mb-4">API Call Form</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium" htmlFor="url">
            URL
          </label>
          <input
            id="url"
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium" htmlFor="path">
            Path
          </label>
          <input
            id="path"
            type="text"
            value={path}
            onChange={(e) => setPath(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium" htmlFor="cookieString">
            Cookie String
          </label>
          <textarea
            id="cookieString"
            value={cookieString}
            onChange={(e) => setCookieString(e.target.value)}
            className="w-full h-96 px-4 py-2 border border-gray-300 rounded-md"
            required
          >{cookieString}</textarea>
        </div>

        <div>
          <button
            type="submit"
            disabled={loading}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-md"
          >
            {loading ? "Loading..." : "Submit"}
          </button>
        </div>
      </form>

      {response && <div className="mt-4 p-4 bg-gray-200">{JSON.stringify(response)}</div>}
    </div>
  );
};

export default App;
