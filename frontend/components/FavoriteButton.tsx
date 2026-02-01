"use client";

import { useState, useEffect } from "react";
import { favoritesApi } from "@/services/api";

interface FavoriteButtonProps {
  companyId: number;
  companyName: string;
}

export default function FavoriteButton({
  companyId,
  companyName,
}: FavoriteButtonProps) {
  const [isFavorite, setIsFavorite] = useState(false);
  const [favoriteId, setFavoriteId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    checkFavoriteStatus();
  }, [companyId]);

  const checkFavoriteStatus = async () => {
    try {
      const favorites = await favoritesApi.getAll();
      const favorite = favorites.find((f) => f.company_id === companyId);
      if (favorite) {
        setIsFavorite(true);
        setFavoriteId(favorite.id);
      } else {
        setIsFavorite(false);
        setFavoriteId(null);
      }
    } catch (error) {
      console.error("Failed to check favorite status:", error);
    }
  };

  const handleToggle = async () => {
    setIsLoading(true);
    try {
      if (isFavorite && favoriteId) {
        // お気に入りから削除
        await favoritesApi.delete(favoriteId);
        setIsFavorite(false);
        setFavoriteId(null);
      } else {
        // お気に入りに追加
        const newFavorite = await favoritesApi.create({ company_id: companyId });
        setIsFavorite(true);
        setFavoriteId(newFavorite.id);
      }
    } catch (error) {
      console.error("Failed to toggle favorite:", error);
      alert("お気に入りの操作に失敗しました");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleToggle}
      disabled={isLoading}
      className={`btn flex items-center space-x-2 transition-smooth transform hover:scale-105 ${
        isFavorite
          ? "bg-yellow-100 text-yellow-700 hover:bg-yellow-200 focus:ring-yellow-400"
          : "bg-gray-100 text-gray-700 hover:bg-gray-200 focus:ring-gray-400"
      }`}
      title={isFavorite ? "お気に入りから削除" : "お気に入りに追加"}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className={`h-5 w-5 transition-transform duration-300 ${
          isFavorite ? "scale-110" : ""
        }`}
        fill={isFavorite ? "currentColor" : "none"}
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={2}
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
        />
      </svg>
      <span className="text-sm font-medium">
        {isFavorite ? "お気に入り済み" : "お気に入り"}
      </span>
    </button>
  );
}
