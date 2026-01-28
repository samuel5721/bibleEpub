window.BibleDOM = (() => {
	function verseIdFromFootnoteId(footnote) {
			const fid = (footnote?.getAttribute('id') || '');
			const m = fid.match(/([1-3]?[A-Z]{2,3})\.(\d+)\.(\d+)/);
			return m ? `${m[1]}.${m[2]}.${m[3]}` : null;
	}

	function visibleLenOfRange(range) {
			const frag = range.cloneContents();
			const tmp = document.createElement('div');
			tmp.appendChild(frag);
			return (tmp.textContent || '').length;
	}

	function getFootnoteIndexInVerse(footnoteEl) {
			const footnoteId = footnoteEl?.getAttribute('id') || '';
			const verseId = verseIdFromFootnoteId(footnoteEl);
			if (!verseId) return 0;

			const allFootnotesInVerse = Array.from(
					document.querySelectorAll(`[class*="ftext hidden"][id*="${CSS.escape(verseId)}"]`)
			);

			const index = allFootnotesInVerse.indexOf(footnoteEl);
			return index >= 0 ? index : 0;
	}

	function findNthMarkerByVerseId(verseId, index) {
			const esc = CSS.escape(verseId);
			const markers = Array.from(
					document.querySelectorAll(`span.ft[class~="${esc}"]`)
			);
			return markers[index] || markers[0] || null;
	}

	// 수정: 마커가 속한 모든 관련 컨테이너가 아닌, 
	// 같은 절의 모든 verse-span을 문서 순서대로 가져오기
	function getAllVerseTextSpans(verseId) {
			// 해당 절의 모든 verse-span 찾기 (절 번호 제외)
			const spans = Array.from(
					document.querySelectorAll(`.verse-span[data-verse-id="${CSS.escape(verseId)}"]`)
			).filter(s => !s.querySelector('.v'));
			
			return spans;
	}

	function getCharOffsetBeforeFootnote(footnoteEl) {
			if (!footnoteEl) return 0;

			const verseId = verseIdFromFootnoteId(footnoteEl);
			if (!verseId) return 0;

			const footnoteIndex = getFootnoteIndexInVerse(footnoteEl);
			const marker = findNthMarkerByVerseId(verseId, footnoteIndex);
			if (!marker) return 0;

			// 수정: 해당 절의 모든 verse-span을 가져옴
			const spans = getAllVerseTextSpans(verseId);
			if (!spans.length) return 0;

			let count = 0;

			for (const s of spans) {
					// 마커가 span 안에 있는 경우
					if (s.contains(marker)) {
							const r = document.createRange();
							r.selectNodeContents(s);
							r.setEndBefore(marker);
							count += visibleLenOfRange(r);
							return count;
					}

					// 마커가 span의 형제 요소인 경우도 체크
					// span과 marker의 부모가 같고, marker가 span 바로 다음에 오는 경우
					if (s.parentElement === marker.parentElement) {
							const siblings = Array.from(s.parentElement.children);
							const spanIdx = siblings.indexOf(s);
							const markerIdx = siblings.indexOf(marker);
							
							if (markerIdx >= 0 && spanIdx < markerIdx) {
									// 마커가 이 span 뒤에 형제로 존재
									// 이 span의 모든 텍스트를 더하고 계속
									count += (s.innerText || s.textContent || '').length;
									continue;
							} else if (markerIdx >= 0 && spanIdx === markerIdx - 1) {
									// 마커가 바로 다음 형제
									count += (s.innerText || s.textContent || '').length;
									return count;
							}
					}

					// 문서 순서 비교
					const pos = s.compareDocumentPosition(marker);
					const spanAfterMarker = !!(pos & Node.DOCUMENT_POSITION_PRECEDING);
					
					if (spanAfterMarker) {
							// 이 span이 마커보다 뒤에 있으면 중단
							return count;
					}

					// 마커가 span 뒤에 있으면 전체 텍스트 누적
					count += (s.innerText || s.textContent || '').length;
			}

			return count;
	}

	function debugFootnote(footnoteEl) {
			const verseId = verseIdFromFootnoteId(footnoteEl);
			const footnoteIndex = getFootnoteIndexInVerse(footnoteEl);
			const marker = verseId ? findNthMarkerByVerseId(verseId, footnoteIndex) : null;
			const spans = verseId ? getAllVerseTextSpans(verseId) : [];
			
			return {
					footnote_id: footnoteEl?.getAttribute('id') || null,
					verseId,
					footnote_index: footnoteIndex,
					marker_found: !!marker,
					marker_class: marker?.getAttribute('class') || null,
					marker_parent: marker?.parentElement?.tagName || null,
					spans_len: spans.length,
					spans_text: spans.map(s => (s.textContent || '').substring(0, 30))
			};
	}

	return {
			getCharOffsetBeforeFootnote,
			debugFootnote
	};
})();