"use client";

import { useState } from "react";
import { CompanySearchResult } from "@/types/company";
import { companiesApi } from "@/services/api";

interface SearchBarProps {
  onSelectCompany?: (company: CompanySearchResult) => void;
}

export default function SearchBar({ onSelectCompany }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<CompanySearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const handleSearch = async () => {
    if (query.length === 0) {
      setResults([]);
      setShowResults(false);
      return;
    }

    setIsLoading(true);
    try {
      const searchResults = await companiesApi.search(query);
      setResults(searchResults);
      setShowResults(true);
    } catch (error) {
      console.error("Search error:", error);
      setResults([]);
      setShowResults(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  const handleSelectCompany = (company: CompanySearchResult) => {
    setQuery("");
    setShowResults(false);
    if (onSelectCompany) {
      onSelectCompany(company);
    }
  };

  return (
    <div className="relative w-full max-w-2xl">
      <div className="flex gap-2">
        <div className="relative flex-1">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="銘柄コードまたは企業名を入力..."
            className="input transition-smooth hover:border-primary/50 text-gray-900"
          />
        </div>
        <button
          onClick={handleSearch}
          disabled={isLoading || query.length === 0}
          className="btn btn-primary px-6 whitespace-nowrap"
        >
          {isLoading ? (
            <div className="flex items-center gap-2">
              <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
              検索中
            </div>
          ) : (
            "検索"
          )}
        </button>
      </div>

      {/* 検索結果 */}
      {showResults && results.length > 0 && (
        <div className="absolute z-10 w-full mt-2 bg-white border border-gray-200 rounded-lg shadow-lg max-h-96 overflow-y-auto animate-fadeInDown">
          {results.map((company) => (
            <button
              key={company.id}
              onClick={() => handleSelectCompany(company)}
              className="w-full px-4 py-3 text-left hover:bg-blue-50 transition-smooth border-b border-gray-100 last:border-b-0 hover-lift"
            >
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-semibold text-gray-900">
                    {company.stock_code}
                  </span>
                  <span className="ml-2 text-gray-700">{company.name}</span>
                </div>
                {company.industry && (
                  <span className="text-sm text-gray-500">{company.industry}</span>
                )}
              </div>
            </button>
          ))}
        </div>
      )}

      {/* 検索結果なし */}
      {showResults && results.length === 0 && !isLoading && (
        <div className="absolute z-10 w-full mt-2 bg-white border border-gray-200 rounded-lg shadow-lg p-4 text-center text-gray-500 animate-fadeInDown">
          該当する銘柄が見つかりませんでした
        </div>
      )}
    </div>
  );
}
