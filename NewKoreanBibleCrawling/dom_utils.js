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
	
		function findMarkerByVerseId(verseId) {
			// <span class="ft GEN.1.1">
			// [class~="GEN.1.1"] 공백으로 분리된 다음과 같은 클래스를 찾는다
			const esc = CSS.escape(verseId);
			return document.querySelector(`span.ft[class~="${esc}"]`);
		}
	
		function findTextContainer(marker) {
			// 본문 블록(단락/인용) 우선
			return (
				marker.closest('.p, .m, .q1') ||
				marker.closest('[class*="p"], [class*="m"], [class*="q"]') ||
				marker.parentElement
			);
		}
	
		function getVerseTextSpansWithin(container, verseId) {
			// 컨테이너 내부에서 해당 절의 본문 텍스트 span들을 찾는다
			// (.v) span 제외 (verse num)
			const spans = Array.from(container.querySelectorAll(`.verse-span[data-verse-id="${CSS.escape(verseId)}"]`))
				.filter(s => !s.querySelector('.v'));
			return spans;
		}
	
		function getCharOffsetBeforeFootnote(footnoteEl) {
			if (!footnoteEl) return 0;
	
			const verseId = verseIdFromFootnoteId(footnoteEl);
			if (!verseId) return 0;
	
			const marker = findMarkerByVerseId(verseId);
			if (!marker) return 0;
	
			const container = findTextContainer(marker);
			if (!container) return 0;
	
			const spans = getVerseTextSpansWithin(container, verseId);
			if (!spans.length) return 0;
	
			// - marker는 보통 container 안의 어떤 위치에 존재합니다. spans의 내용을 앞에서부터 누적하다가 각주 앞에서 끊고 본문 전체를 리턴합니다.
	
			let count = 0;
	
			for (const s of spans) {
				// marker가 이 span 안에 있으면 그 span에서 marker 직전까지만 잰다
				if (s.contains(marker)) {
					const r = document.createRange();
					r.selectNodeContents(s);
					r.setEndBefore(marker);
					count += visibleLenOfRange(r);
					return count;
				}
	
				// marker가 span 밖인데, marker가 span중간에 끼는 구조(예: span 다음에 marker가 독립 노드로 존재)일 수 있음
				// marker가 span 뒤에 나오기 전까지의 span은 전부 더함.
				// marker가 span 앞에 나오면(즉, marker가 더 앞이면) 여기까지 더하면 안 되므로 문서 순서를 비교한다.
				const pos = s.compareDocumentPosition(marker);
				const spanAfterMarker = !!(pos & Node.DOCUMENT_POSITION_PRECEDING); // s가 marker보다 뒤에 있음
				if (spanAfterMarker) {
					// marker가 이미 앞에 있음 -> 더하면 안 됨
					return count;
				}
	
				count += (s.innerText || s.textContent || '').length;
			}
	
			// spans를 다 돌았는데도 marker를 못 만났다면
			// marker가 container 안이지만 verse spans와 분리되어 있을 수 있음 → 지금까지 누적한 값 반환
			return count;
		}
	
		function debugFootnote(footnoteEl) {
			const verseId = verseIdFromFootnoteId(footnoteEl);
			const marker = verseId ? findMarkerByVerseId(verseId) : null;
			const container = marker ? findTextContainer(marker) : null;
			const spans = (container && verseId) ? getVerseTextSpansWithin(container, verseId) : [];
			return {
				footnote_id: footnoteEl?.getAttribute('id') || null,
				verseId,
				marker_found: !!marker,
				marker_class: marker?.getAttribute('class') || null,
				container_tag: container?.tagName || null,
				container_class: container?.getAttribute('class') || null,
				spans_len: spans.length,
				marker_in_container: container ? container.contains(marker) : false
			};
		}
	
		return {
			getCharOffsetBeforeFootnote,
			debugFootnote
		};
	})();
	